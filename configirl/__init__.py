# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright 2019 Sanhe Hu <https://github.com/MacHu-GWU/configirl-project>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This is a python config management tool to manage config parameter in
centralized place. The purpose of this tool is to avoid maintain complex
config/paramater handling logic in shell script, cloudformation, terraform
and any other devops tools. Instead, we manage that in Python.

Since Python is a full featured general programming language and it is
available on any Mac / Linux machine.

It allows different DevOps tools to easily talk to each other via JSON.

This library implemented in pure Python with no dependencies.
"""

from __future__ import print_function

__version__ = "0.0.3"
__short_description__ = "Package short description."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

import os
import re
import sys
import json
import copy
import inspect
from collections import OrderedDict

if sys.version_info.major >= 3 and sys.version_info.minor >= 5:  # pragma: no cover
    from typing import Dict


def strip_comment_line_with_symbol(line, start):
    """
    Strip comments from line string.
    """
    parts = line.split(start)
    counts = [len(re.findall(r'(?:^|[^"\\]|(?:\\\\|\\")+)(")', part))
              for part in parts]
    total = 0
    for nr, count in enumerate(counts):
        total += count
        if total % 2 == 0:
            return start.join(parts[:nr + 1]).rstrip()
    else:  # pragma: no cover
        return line.rstrip()


def strip_comments(string, comment_symbols=frozenset(('#', '//'))):
    """
    Strip comments from json string.

    :param string: A string containing json with comments started by comment_symbols.
    :param comment_symbols: Iterable of symbols that start a line comment (default # or //).
    :return: The string with the comments removed.
    """
    lines = string.splitlines()
    for k in range(len(lines)):
        for symbol in comment_symbols:
            lines[k] = strip_comment_line_with_symbol(lines[k], start=symbol)
    return '\n'.join(lines)


def read_text(abspath, encoding="utf-8"):
    """
    :type abspath: str
    :type encoding: str
    :rtype: str
    """
    with open(abspath, "rb") as f:
        return f.read().decode(encoding)


def write_text(text, abspath, encoding="utf-8"):
    """
    :type text: str
    :type abspath: str
    :type encoding: str
    :rtype: None
    """
    with open(abspath, "wb") as f:
        return f.write(text.encode(encoding))


def json_loads(text):
    return json.loads(strip_comments(text))


def json_dumps(data):
    return json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)


def add_metaclass(metaclass):
    """
    Class decorator for creating a class with a metaclass.

    This method is copied from six.py
    """

    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        if hasattr(cls, '__qualname__'):
            orig_vars['__qualname__'] = cls.__qualname__
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return wrapper


try:
    # python3 renamed copy_reg to copyreg
    import copyreg
except ImportError:  # pragma: no cover
    import copy_reg as copyreg


class Sentinel(object):
    _existing_instances = {}

    def __init__(self, name):
        super(Sentinel, self).__init__()
        self._name = name
        self._existing_instances[self._name] = self

    def __repr__(self):
        return "<{0}>".format(self._name)

    def __getnewargs__(self):
        return (self._name,)

    def __new__(cls, name, obj_id=None):  # obj_id is for compatibility with previous versions
        existing_instance = cls._existing_instances.get(name)
        if existing_instance is not None:
            return existing_instance
        return super(Sentinel, cls).__new__(cls)


# obj_id is for compat. with prev. versions
def _sentinel_unpickler(name, obj_id=None):
    if name in Sentinel._existing_instances:
        return Sentinel._existing_instances[name]
    return Sentinel(name)


def _sentinel_pickler(sentinel):
    return _sentinel_unpickler, sentinel.__getnewargs__()


copyreg.pickle(Sentinel, _sentinel_pickler, _sentinel_unpickler)

NOTHING = Sentinel("NOTHING")


class ValueNotSetError(Exception):
    """
    Raises when trying to get value of a field that have not set value before.
    """
    pass


class DerivableSetValueError(Exception):
    """
    Raises when trying to set value for Derivable Field.
    """
    pass


#
class Field(object):
    """
    Base class for config value field.

    :type dont_dump: bool
    :param dont_dump: if true, then you can't get the value if ``check_dont_dump = True``
        in :meth:`BaseConfigClass.to_dict` and :meth:`BaseConfigClass.to_json`.
        this prevent from writing sensitive information to file

    :type printable: bool
    :param printable: if False, then it will not be displayed with
        :meth:`BaseConfigClass.pprint`
    """
    _creation_index = 0

    def __init__(self,
                 default=NOTHING,
                 dont_dump=False,
                 printable=True):
        self.name = None
        self._value = default

        self.dont_dump = dont_dump  # type: bool
        self.printable = printable  # type: bool

        self._config_object = NOTHING  # type: BaseConfigClass
        self._creation_index = Field._creation_index  # type: int
        Field._creation_index += 1

        self._getter_method = NOTHING  # type: callable

    def __repr__(self):
        return "{}(name={!r}, value={!r})".format(self.__class__.__name__, self.name, self._value)

    def set_value(self, value):
        raise DerivableSetValueError(
            "Derivable.set_value() method should never bee called")

    def get_value(self, check_dont_dump=False, check_printable=False):
        """
        Since the derivable

        :param config_instance:
        :param check_dont_dump:
        :param check_printable:
        :return:

        **CN Doc**

        对于 Constant Field:

        - 如果: self.value = NOTHING, 同时 .set_value(...) 方法从来没有被调用过.
        - 如果: self.value 不等于 NOTHING, 说明 .set_value(...) 方法被吊用过, 则
            返回 self.value

        对于 Derivable Field:

        - 如果: self._getter_method() 没有成功

        """
        if self._config_object is NOTHING:
            raise AttributeError("Field.get_value() can't be called without "
                                 "initialized with ")
        if check_dont_dump:
            if self.dont_dump:
                raise DontDumpError
        if check_printable:
            if not self.printable:
                return "***HIDDEN***"

        if self._getter_method is NOTHING:
            if self._value is NOTHING:
                raise ValueNotSetError(
                    "{}.{} has not set a value yet!".format(
                        self.__class__.__name__, self.name
                    )
                )
            else:
                return self._value
        else:
            return self._getter_method(self._config_object)

    def _validate_method(self, config_object, value):
        return True

    def validator(self, method):
        """
        a decorator to bind validate method.

        :type method: callable
        :param method: a callable function like ``method(self, value)``
            that take ``self`` as first parameters representing the config object.
            ``value`` as second parameters to represent the value you want to validate.
        """
        self._validate_method = method

    def validate(self, *args, **kwargs):
        """
        An abstract method executes the validator method.
        """
        self._validate_method(self._config_object, self.get_value())


class DontDumpError(Exception):
    """
    Raises when trying to dump a ``dont_dump=True`` config value.
    """
    pass


class Constant(Field):
    """
    Constant Value.
    """

    def set_value(self, value):
        self._value = value


class Derivable(Field):
    """
    Derivable Value.
    """

    def getter(self, method):
        self._getter_method = method


def is_instance_or_subclass(val, class_):
    """Return True if ``val`` is either a subclass or instance of ``class_``."""
    try:
        return issubclass(val, class_)
    except TypeError:
        return isinstance(val, class_)


def _get_fields(attrs, field_class, pop=False, ordered=False):
    """Get fields from a class. If ordered=True, fields will sorted by creation index.
    :param attrs: Mapping of class attributes
    :param type field_class: Base field class
    :param bool pop: Remove matching fields
    """
    fields = [
        (field_name, field_value)
        for field_name, field_value in attrs.items()
        if is_instance_or_subclass(field_value, field_class)
    ]
    if pop:  # pragma: no cover
        for field_name, _ in fields:
            del attrs[field_name]
    if ordered:
        fields.sort(key=lambda pair: pair[1]._creation_index)
    return fields


def _get_fields_by_mro(klass, field_class, ordered=False):
    """Collect fields from a class, following its method resolution order. The
    class itself is excluded from the search; only its parents are checked. Get
    fields from ``_declared_fields`` if available, else use ``__dict__``.
    :param type klass: Class whose fields to retrieve
    :param type field_class: Base field class
    """
    mro = inspect.getmro(klass)
    # Loop over mro in reverse to maintain correct order of fields
    return sum(
        (
            _get_fields(
                getattr(base, "_declared_fields", base.__dict__),
                field_class,
                ordered=ordered,
            )
            for base in mro[:0:-1]
        ),
        [],
    )


class ConfigMeta(type):
    def __new__(cls, name, bases, attrs):
        cls_fields = _get_fields(attrs, Field, pop=False, ordered=True)
        klass = super(ConfigMeta, cls).__new__(cls, name, bases, attrs)
        inherited_fields = _get_fields_by_mro(klass, Field, ordered=True)

        # Assign _declared_fields on class
        klass._declared_fields = OrderedDict(inherited_fields + cls_fields)
        klass._constant_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Constant)
        ])
        klass._deriable_fields = OrderedDict([
            (name, field)
            for name, field in klass._declared_fields.items()
            if isinstance(field, Derivable)
        ])
        for name, field in klass._declared_fields.items():
            field.name = name
        return klass


class BaseConfigClass(object):
    """

    - :attr:`BaseConfigClass._declared_fields`:
    - :attr:`BaseConfigClass._constant_fields`:
    - :attr:`BaseConfigClass._deriable_fields`:
    """
    _declared_fields = OrderedDict()  # type: Dict[str: Field]
    _constant_fields = OrderedDict()  # type: Dict[str: Constant]
    _deriable_fields = OrderedDict()  # type: Dict[str: Derivable]

    # --- constructor method
    def __init__(self, **kwargs):
        self.__pre_hook_init__()
        for name, field in self._declared_fields.items():
            if name in kwargs:
                field.set_value(kwargs[name])
            field._config_object = self

    def __pre_hook_init__(self):
        """
        All declared fields is a mutable :class:`Field` Instance, defined
        in Class level. So when you creating a new instance, the class
        level fields have to be deep copied to the config instance.
        """
        self._declared_fields = OrderedDict([
            (attr, copy.deepcopy(field))
            for attr, field in self._declared_fields.items()
        ])
        self._constant_fields = OrderedDict([
            (attr, self._declared_fields[attr])
            for attr, _ in self._constant_fields.items()
        ])
        self._deriable_fields = OrderedDict([
            (attr, self._declared_fields[attr])
            for attr, _ in self._deriable_fields.items()
        ])

        for attr, field in self._declared_fields.items():
            setattr(self, attr, field)

    @classmethod
    def from_dict(cls, dct):
        """
        Only read constant config variables from json file.

        :type dct: dict
        :rtype: BaseConfig
        """
        config = cls()
        for key, value in dct.items():
            if key in config._constant_fields:
                config._constant_fields[key].set_value(value)
        return config

    @classmethod
    def from_json(cls, json_str):
        """
        :type json_str: str
        :rtype: BaseConfig
        """
        return cls.from_dict(json.loads(strip_comments(json_str)))

    def update(self, dct):
        """
        Update constance config values from dictionary.

        :type dct: dict

        :rtype: None
        """
        for key, value in dct.items():
            if key in self._constant_fields:
                self._constant_fields[key].set_value(value)

    def update_from_raw_json_file(self):
        """
        Update constance config values from the :attr:`BaseConfigClass.CONFIG_RAW_JSON_FILE`.
        """
        dct = json.loads(strip_comments(read_text(self.CONFIG_RAW_JSON_FILE)))
        self.update(dct)

    def to_dict(self, check_dont_dump=True, check_printable=False):
        dct = OrderedDict()
        for attr, value in self._declared_fields.items():
            try:
                dct[attr] = value.get_value(
                    check_dont_dump=check_dont_dump, check_printable=check_printable)
            except DontDumpError:
                pass
            except Exception as e:
                raise e
        return dct

    def to_json(self, check_dont_dump=True, check_printable=False):
        return json.dumps(
            self.to_dict(check_dont_dump=check_dont_dump,
                         check_printable=check_printable),
            indent=4, sort_keys=False,
        )

    def __repr__(self):
        return "Config({})".format(
            self.to_json(check_dont_dump=False, check_printable=True)
        )

    def pprint(self):
        print(self.__repr__())

    def validate(self):
        for field in self._declared_fields.values():
            field.validate()

    # --- config file path management
    CONFIG_DIR = NOTHING  # type: str

    def _join_config_dir(self, filename):
        if self.CONFIG_DIR is NOTHING:
            raise ValueError("You have to specify `{}.CONFIG_DIR`!".format(
                self.__class__.__name__))
        if not os.path.exists(self.CONFIG_DIR):
            raise ValueError("`{}.CONFIG_DIR` ('{}') doesn't exist!".format(
                self.__class__.__name__, self.CONFIG_DIR))
        return os.path.join(self.CONFIG_DIR, filename)

    @property
    def CONFIG_RAW_JSON_FILE(self):
        return self._join_config_dir("config-raw.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_PYTHON(self):
        return self._join_config_dir("config-final-for-python.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT(self):
        return self._join_config_dir("config-final-for-shell-script.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION(self):
        return self._join_config_dir("config-final-for-cloudformation.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SAM(self):
        return self._join_config_dir("config-final-for-sam.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS(self):
        return self._join_config_dir("config-final-for-serverless.json")

    @property
    def CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM(self):
        return self._join_config_dir("config-final-for-terraform.json")

    # --- Custom logic for different devops tools
    def to_python_json_config_data(self):
        return self.to_dict()

    def to_shell_script_config_data(self):
        return self.to_dict()

    def to_cloudformation_config_data(self):
        def to_big_camel_case(text):
            return "".join([
                word[0].upper() + word[1:].lower()
                for word in text.split("_")
            ])

        return OrderedDict([
            (to_big_camel_case(key), value)
            for key, value in self.to_dict().items()
        ])

    def to_sam_config_data(self):
        return self.to_dict()

    def to_serverless_config_data(self):
        return self.to_dict()

    def to_terraform_config_data(self):
        return self.to_dict()

    def _dump_for_xxx_config_file(self,
                                  to_config_data_meth,
                                  config_json_file_path):
        json_str = json_dumps(to_config_data_meth())
        write_text(json_str, config_json_file_path)

    def dump_python_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_python_json_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_PYTHON,
        )

    def dump_shell_script_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_shell_script_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SHELL_SCRIPT,
        )

    def dump_cloudformation_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_cloudformation_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_CLOUDFORMATION,
        )

    def dump_sam_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_sam_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SAM,
        )

    def dump_serverless_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_serverless_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_SERVERLESS,
        )

    def dump_terraform_json_config_file(self):
        self._dump_for_xxx_config_file(
            self.to_terraform_config_data,
            self.CONFIG_FINAL_JSON_FILE_FOR_TERRAFORM,
        )


@add_metaclass(ConfigMeta)
class ConfigClass(BaseConfigClass):
    pass


__all__ = ["ConfigClass", "Constant", "Derivable"]
