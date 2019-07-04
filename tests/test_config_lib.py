# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from os import environ, path
from os.path import join, abspath, dirname, basename
from configirl import (
    ConfigClass, Constant, Derivable,
    DontDumpError, DeriableSetValueError,
)


class Config1(ConfigClass):
    CONFIG_DIR = path.dirname(__file__)

    PROJECT_NAME = Constant()
    STAGE = Constant()


class Config2(Config1):
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_project_name_slug(self):
        return self.PROJECT_NAME.get_value().replace("_", "-")

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_environment_name(self):
        return "{}-{}".format(
            self.PROJECT_NAME_SLUG.get_value(),
            self.STAGE.get_value(),
        )

    GITHUB_USERNAME = Constant()
    GITHUB_PASSWORD = Constant(printable=False)

    @GITHUB_PASSWORD.validator
    def check_github_password(self, value):
        if len(value) < 16:
            raise ValueError(
                "GITHUB_PASSWORD has to be more than 16 characters!")

    LAPTOP_PASSWORD = Constant(dont_dump=True, printable=False)

    RUNTIME_NAME = Derivable()

    @RUNTIME_NAME.getter
    def get_runtime_name(self):
        if "CIRCLECI" in environ:
            return "circleci"
        elif "LAMBDA_RUNTIME_DIR" in environ:
            return "lambda"
        else:
            return "local"


class Config(Config2):
    pass


config = Config(
    PROJECT_NAME="my_project",
    GITHUB_USERNAME="alice",
    GITHUB_PASSWORD="mypassword",
)
config.STAGE.set_value("dev")
config.update(dict(
    LAPTOP_PASSWORD="adminpassword",
))


class TestConfigClass(object):
    def test(self):
        assert config.PROJECT_NAME.get_value() == "my_project"
        assert config.STAGE.get_value() == "dev"
        assert config.PROJECT_NAME_SLUG.get_value() == "my-project"
        assert config.ENVIRONMENT_NAME.get_value() == "my-project-dev"
        assert config.LAPTOP_PASSWORD.get_value() == "adminpassword"
        assert config.RUNTIME_NAME.get_value(
        ) in ["circleci", "lambda", "local"]

    def test_repr_and_printable_option(self):
        assert "mypassword" not in config.__repr__()

    def test_dont_dump_option(self):
        data = config.to_dict()
        assert "GITHUB_PASSWORD" in data
        assert "LAPTOP_PASSWORD" not in data

    def test_deriable_set_value_error(self):
        with raises(DeriableSetValueError):
            config.ENVIRONMENT_NAME.set_value("env name")

    def test_validate(self):
        try:
            config.validate()
        except Exception as e:
            assert "GITHUB_PASSWORD has to be more than 16 characters!" in str(
                e)

    def test_work_with_config_files(self):
        config1 = Config()
        config1.update_from_raw_json_file()
        config1.validate()

        config1.dump_python_json_config_file()
        config1.dump_shell_script_json_config_file()
        config1.dump_cloudformation_json_config_file()
        config1.dump_sam_json_config_file()
        config1.dump_serverless_json_config_file()
        config1.dump_terraform_json_config_file()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
