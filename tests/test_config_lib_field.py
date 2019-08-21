# -*- coding: utf-8 -*-

"""
Test field related options
"""

import pytest
from pytest import raises
from configirl import ConfigClass, Constant, Derivable
from configirl import ValueNotSetError, DontDumpError, DerivableSetValueError


class Config(ConfigClass):
    PROJECT_NAME = Constant()
    STAGE = Constant()

    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_PROJECT_NAME_SLUG(self):
        return self.PROJECT_NAME.get_value().replace("_", "-")

    @PROJECT_NAME_SLUG.validator
    def check_PROJECT_NAME_SLUG(self, value):
        if "_" in value:
            raise ValueError("you can't use `_` in slugifie name!")

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return "{}-{}".format(
            self.PROJECT_NAME_SLUG.get_value(),
            self.STAGE.get_value(),
        )

    GIT_PASSWORD = Constant(printable=False)

    METADATA = Constant(dont_dump=True)


def test_value_not_set_error():
    """
    Test been correctly raised.
    """
    conf = Config()

    with raises(ValueNotSetError):
        conf.PROJECT_NAME.get_value()

    with raises(ValueNotSetError):
        conf.PROJECT_NAME_SLUG.get_value()

    try:
        conf.PROJECT_NAME_SLUG.get_value()
    except Exception as e:
        assert "PROJECT_NAME" in str(e)
        assert "PROJECT_NAME_SLUG" in str(e)

    with raises(ValueNotSetError):
        conf.PROJECT_NAME_SLUG.get_value()

    try:
        conf.ENVIRONMENT_NAME.get_value()
    except Exception as e:
        assert "PROJECT_NAME" in str(e)
        assert "PROJECT_NAME_SLUG" in str(e)
        assert "ENVIRONMENT_NAME" in str(e)


def test_dont_dump_error():
    """
    Test DontDumpError been correctly raised.
    """
    conf = Config()
    with raises(DontDumpError):
        conf.METADATA.get_value(check_dont_dump=True)


def test_derivable_set_value_error():
    """
    Test DerivableSetValueError been correctly raised.
    """
    with raises(DerivableSetValueError):
        Config(ENVIRONMENT_NAME="my-project-dev")

    conf = Config()
    with raises(DerivableSetValueError):
        conf.ENVIRONMENT_NAME.set_value("my-project-dev")


def test_get_value_from_env():
    import os

    os.environ["CONFIGIRL_PROJECT_NAME"] = "configirl"
    conf = Config()
    PREFIX = "CONFIGIRL_"
    assert conf.PROJECT_NAME.get_value_from_env(PREFIX) == "configirl"


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
