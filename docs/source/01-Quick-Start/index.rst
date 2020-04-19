Quick Start
==============================================================================

.. contents::
    :depth: 1
    :local:


Install ``configirl``
------------------------------------------------------------------------------

``configirl`` is just a Python Package published on PyPI. The easiest way to install it by ``pip install configirl``.

I recommend to install ``configirl`` once to your **GLOBAL python interpreter**, this allows your non virtual env bash script also easily integrates with ``configirl``.

To validate if it is installed correctly, just type ``which configirl`` (MacOS, Linux) or ``where configirl`` (Windows). Or get into Python interactive console and type ``import configirl``.


Config Declaration
------------------------------------------------------------------------------

Config Declaration module is simply a ``.py`` file that defines a :class:`Config <configirl.ConfigClass>` class, and it's attributes are mostly Config field. There are two type of Config fields:

1. :class:`Constant <configirl.Constant>`: a constant value, a hard coded value.
2. :class:`Derivable <configirl.Derivable>`: a dynamic value, the value could depends on other field, or dynamically retrieved by external data store. Such as AWS Secret Manager, AWS Parameter Store. You have to define the login in a method.

First, import ``configirl``. :class:`configirl.ConfigClass` is the base class of your custom Config class. :class:`configirl.Constant` and :class:`configirl.Derivable` are the config field factory class.

.. code-block:: python

    # content of config.py
    from configirl import ConfigClass, Constant, Derivable

Then, declare your config fields. The syntax is very similar to ORM frameworks. :

.. code-block:: python

    # content of config.py
    from configirl import ConfigClass, Constant, Derivable

    class Config(ConfigClass):
        PROJECT_NAME = Constant()

        # slugified version of your project name
        PROJECT_NAME_SLUG = Derivable()

        @PROJECT_NAME_SLUG.getter
        def get_project_name_slug(self):
            return self.PROJECT_NAME.get_value().replace("_", "-")

        @PROJECT_NAME_SLUG.validator
        def check_project_name_slug(self, value):
            if "_" in value:
                raise ValueError("you can't use `_` in slugifie name!")

        STAGE = Constant() # dev, test, prod

        @STAGE.validator
        def check_stage(self, value):
            if value not in ["dev", "test", "prod"]:
                raise ValueError("{} is an invalid value for STAGE".format(value))

        # environment name is a naming convention prefix that help you isolate
        # resources belongs to different environment.
        ENVIRONMENT_NAME = Derivable()

        @ENVIRONMENT_NAME.getter
        def get_environment_name(self):
            return "{}-{}".format(
                self.PROJECT_NAME_SLUG.get_value(),
                self.STAGE.get_value(),
            )


Initialize Config Object
------------------------------------------------------------------------------

``configirl`` provides lots of methods to load values into config object.

1. **Pass in value for Constant field directly in keywords style**.

.. code-block:: python

    config = Config(PROJECT_NAME="my_project", STAGE="dev")
    print(config)

Output::

    Config({
        "PROJECT_NAME": "my_project",
        "PROJECT_NAME_SLUG": "my-project",
        "STAGE": "dev",
        "ENVIRONMENT_NAME": "my-project-dev"
    })

Don't worry about leaking sensitive information with ``print()``. See this.

.. note::

    You can only pass value to :class:`configirl.Constant` field. **Passing value to** :class:`configirl.Derivable` **is forbidden**.

.. note::

    Passing in undefined value is allowed. But it will be ignored in initialization. For example:

    .. code-block:: python

        config = Config(..., UNDEFINED_FIELD="nothing")


2. **Initialize an empty Constant object, and call** :meth:`configirl.Constant.set_value` **method to update Constant field afterwards**.

.. code-block:: python

    config = Config()
    config.PROJECT_NAME.set_value("my_project")
    config.STAGE.set_value("dev")

3. **You can call** :meth:`configirl.BaseConfigClass.update` **method to update multiple** :class:`Constant <configirl.Constant>` **field at one time**.

.. code-block:: python

    config = Config()
    config.update(dict(
        PROJECT_NAME="my_project", STAGE="dev",
    ))

4. **You can call** :meth:`configirl.BaseConfigClass.update_from_raw_json_file` **method to load multiple** :class:`Constant <configirl.Constant>` **field from a JSON file at one time. JSON file could includes COMMENTS, to makes your config json file more maintainable**.

.. code-block:: javascript

    // content of my-config.json
    {
        "PROJECT_NAME": "my_project",
        // only allow "dev" | "test" | "prod"
        "STAGE": "dev"
    }

.. code-block:: python

    config = Config()
    config.update_from_raw_json("my-config.json")

5. **You can call** :meth:`configirl.BaseConfigClass.update_from_env_var` **method to load multiple** :class:`Constant <configirl.Constant>` **field from ENVIRONMENT VARIABLE at one time. You can pass in prefix argument to avoid ENV VAR naming collision**.


.. code-block:: bash

    >>> env
    MY_PROJECT_PROJECT_NAME=my_project
    MY_PROJECT_STAGE=dev

.. code-block:: python

    config = Config()
    config.update_from_env_var(prefix="MY_PROJECT_")

6. **Load data from external data store, such as database, AWS Parameter Store, AWS Secret Manager** (simplify sensitive data management). The idea is simple, for database, you can use `sqlalchemy <https://www.sqlalchemy.org/>`_ library to read the data, for AWS you can use `boto3 <https://aws.amazon.com/sdk-for-python/>`_ library to read the data. And then just pass in data from a dictionary.

All available utility initialization methods:

- :meth:`configirl.BaseConfigClass.from_dict`
- :meth:`configirl.BaseConfigClass.from_json_str`
- :meth:`configirl.BaseConfigClass.from_json_file`
- :meth:`configirl.BaseConfigClass.from_env_var`
- :meth:`configirl.BaseConfigClass.update`
- :meth:`configirl.BaseConfigClass.update_from_raw_json_file`
- :meth:`configirl.BaseConfigClass.update_from_env_var`


.. _int-with-python:

Reference Config Value in Python Application Code
------------------------------------------------------------------------------

Referencing config value in Python Application Code is easy, just call the :meth:`configirl.Field.get_value` method. For example:

.. code-block:: python

    config = Config()
    config.update_from_raw_json("my-config.json")

    if config.STAGE.get_value() == "prod":
        # do production logic
    else:
        # ...

**But for enterprise application, you need some mature pattern from this best practice**.

**About your code file structure, I recommend using this structure**::

    /git-repo-root
        /your_package_name
            /__init__.py
            /config.py
            /config_init.py

``config.py`` only declares your config klass, but doesn't manage anything about initialization. ``config_init.py`` creates the instance of your Config class, and implements the logic that loads data into the config object.

Here are the reasons:

1. You want to be able to test your Config declaration class without really loading data from external resources like database. So it's better to isolate the declaration and initialization.
1. Some fields may need to load data from external resources, which is expensive. some fields is just pure string manipulation or conditional logic flow, which is light. Sometimes you would like to only reuse those 'light' part of your logic. This pattern gives you flexibility to do that.


**Config declaration and initialization**:

Declaration:

.. code-block:: python

    # content of config.py
    from configirl import ConfigClass, Constant, Derivable

    class Config(ConfigClass):
        PROJECT_NAME = Constant()

        ...

Initialization:

.. code-block:: python

    # content of config_init.py
    from .config import Config

    config = Config()
    # implement data loading logic
    ...


**Reference config value in Python Application code**:

.. code-block:: python

    from your_package_name.config_init import config

    if config.STAGE.get_value() == "prod":
        # do production logic
    else:
        # ...


.. _dump-config:

Dump Derived Config Value to Dict data or to File
------------------------------------------------------------------------------

Sometimes you want to pass derived config value to a dict data and perform some manipulation on it. See :meth:`configirl.BaseConfigClass.to_dict` method for more information.

Sometimes you need to dump derived config value to files allow other system like shell script to consume it. See :meth:`configirl.BaseConfigClass.to_json` method for more information.


.. _printable:

Prevent Printing Sensitive Information to Console
------------------------------------------------------------------------------

By default, the build-in ``print()`` function displays all values stored in the config object. For example: ``print(Config.from_json_file("my-config.json"))``

:class:`configirl.Field` has a ``printable`` arg that can hide the data when you print the object. But be aware, there's no way can prevent you from printing data from memory by doing ``print(config.DB_PASSWORD.get_value())``, which is absolutely an anti pattern.

.. code-block:: python

    class Config(ConfigClass):
        DB_PASSWORD = Constant(printable=False)

    config=Config()
    # whatever how you load the data
    ...
    print(config)

Output:

.. code-block:: python

    Config({
        "DB_PASSWORD": "***HIDDEN***"
    })


.. _dont-dump:

Prevent Dump Sensitive Information to Json File
------------------------------------------------------------------------------

:meth:`configirl.BaseConfigClass.to_json`. But you don't want to dump your ``DB_PASSWORD`` to a static file on your server.

:class:`configirl.Field` has a ``dont_dump`` arg that omit some fields when you call hide the data when you call :meth:`configirl.BaseConfigClass.to_dict` and :meth:`configirl.BaseConfigClass.to_json`.

.. code-block:: python

    class Config(ConfigClass):
        DB_PASSWORD = Constant(dont_dump=True)

    config=Config()
    # whatever how you load the data
    ...
    print(config.to_dict())

Output:

.. code-block:: python

    OrderedDict()


.. _cache:

Cache Expensive Dynamic Field
------------------------------------------------------------------------------

Store your config values on professional cloud service like AWS Secret Manager and AWS Parameter store is always the best idea. Data is encrypted, built-in access management, it is secure and highly available.

But makeing API call to external resource may be expensive. Let's say you have 10 Derivable fields stored in single AWS Parameter. You only wants to make one ``aws get-parameter`` API Call to retrieve everything, and never call this again during the life cycle of the config object.

:class:`configirl.Field` has a ``cache`` arg that cache the value at the first time you derive it. Here's an example:

.. code-block:: python

    class Config(ConfigClass):
        SENSITIVE_PARAMETER_DATA = Derivable(dont_dump=True, printable=False, cache=True)

        @SENSITIVE_PARAMETER_DATA.getter
        def get_SENSITIVE_PARAMETER_DATA(self):
            """
            See aws doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter
            """
            return json.loads(boto3.client("ssm").get_parameter(Name="my-param", WithDecryption=True))

        DB_HOST = Derivable()

        @DB_HOST.getter
        def get_DB_HOST(self):
            return self.SENSITIVE_PARAMETER_DATA.get_value()["DB_HOST"]


        DB_PASSWORD = Derivable()

        @DB_PASSWORD.getter
        def get_DB_PASSWORD(self):
            return self.SENSITIVE_PARAMETER_DATA.get_value()["DB_PASSWORD"]


.. _validator:

Custom Validator
------------------------------------------------------------------------------

Data validator is a nice feature preventing you from using malformed config values.

.. code-block:: python

    from configirl import ConfigClass, Constant, Derivable

    ALLOWED_STAGE_VALUES = ["dev", "test", "prod"]

    class Config(object):
        STAGE = Constant()

        @STAGE.validator
        def check_STAGE(self, value):
            if value not in ALLOWED_STAGE_VALUES:
                raise ValueError
