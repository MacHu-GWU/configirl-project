# -*- coding: utf-8 -*-

import pytest
from pytest import raises
from configirl import (
    ConfigClass, Constant, Derivable,
    ValueNotSetError, DerivableSetValueError,
)


def test_get_value_method_been_called_without_class_object():
    class Config(ConfigClass):
        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Derivable()

    with raises(AttributeError):
        Config.PROJECT_NAME.get_value()


def test_deep_copy_field_instance_when_init_class_object():
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
    assert len(set(field_id_list)) == len(field_id_list)


class TestValueNotSetError():
    def test(self):
        class Config(ConfigClass):
            PROJECT_NAME = Constant()

        config = Config()
        with raises(ValueNotSetError):
            config.PROJECT_NAME.get_value()


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

    with raises(ValueNotSetError):
        config.PROJECT_NAME_SLUG.get_value()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
