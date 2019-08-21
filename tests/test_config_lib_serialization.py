# -*- coding: utf-8 -*-

"""
Test to_dict and to_json method and options
"""

import pytest
from os import environ, path
from configirl import ConfigClass, Constant, Derivable
from configirl import ValueNotSetError


class Config(ConfigClass):
    CONFIG_DIR = path.dirname(__file__)

    PROJECT_NAME = Constant()
    STAGE = Constant()

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


class TestConfigClass(object):
    def test_to_dict(self):
        config = Config(
            PROJECT_NAME="my_project",
            STAGE="dev",
            GITHUB_USERNAME="alice",
            GITHUB_PASSWORD="mypassword",
            LAPTOP_PASSWORD="adminpassword",
        )

        # test check_dont_dump option
        assert "LAPTOP_PASSWORD" in config.to_dict(check_dont_dump=False)
        assert "LAPTOP_PASSWORD" not in config.to_dict(check_dont_dump=True)

        # test check_printable option
        assert "HIDDEN" not in config.to_dict(check_printable=False)["GITHUB_PASSWORD"]
        assert "HIDDEN" in config.to_dict(check_printable=True)["GITHUB_PASSWORD"]

        # test prefix option
        for k in config.to_dict(prefix="CONFIGIRL_"):
            assert k.startswith("CONFIGIRL_")

        # test ignore_na option
        config = Config()
        with pytest.raises(ValueNotSetError):
            config.to_dict(ignore_na=False)

        config.to_dict(ignore_na=True)


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
