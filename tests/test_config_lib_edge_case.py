# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from configirl import (
    ConfigClass, Constant, Derivable,
    DerivableSetValueError,
)


def test_get_value_method_been_called_without_class_object():
    class Config(ConfigClass):
        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Derivable()

    with raises(AttributeError):
        Config.PROJECT_NAME.get_value()


def test_deep_copy_field_instance_when_init_class_object():
    """
    Test if Field attribute in the instance Config are actual different entities.

    Because Field defines in Class level and the Field is a mutable object,
    we have to do deep copy when you initiate the config object.
    """

    class Config(ConfigClass):
        PROJECT_NAME = Constant(default="my_project")

    field_id_list = [
        id(Config().PROJECT_NAME),
        id(Config().PROJECT_NAME),
        id(Config(PROJECT_NAME="my_project")),
        id(Config(PROJECT_NAME="my_project")),
        id(Config.from_dict(dict(PROJECT_NAME="my_project"))),
        id(Config.from_dict(dict(PROJECT_NAME="my_project"))),
    ]

    # entity id are different
    assert len(set(field_id_list)) == len(field_id_list)


def test_config_dir():
    class Config(ConfigClass):
        pass

    config = Config()
    with raises(ValueError):
        config.CONFIG_RAW_JSON_FILE

    Config.CONFIG_DIR = "path-not-exists"
    config = Config()
    with raises(ValueError):
        config.CONFIG_RAW_JSON_FILE


def test_derivable_field_get_value_with_no_default():
    class Config(ConfigClass):
        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Derivable()

    config = Config(PROJECT_NAME="my_project")

    with raises(DerivableSetValueError):
        config.PROJECT_NAME_SLUG.set_value("my-project")

    with raises(NotImplementedError) as e:
        config.PROJECT_NAME_SLUG.get_value()
    assert "@PROJECT_NAME_SLUG.getter" in str(e)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
