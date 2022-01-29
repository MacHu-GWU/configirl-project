# -*- coding: utf-8 -*-

"""
Test field related options
"""

import pytest
from pytest import raises

from datetime import datetime
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

    PROJECT_NAME_SUPER_SLUG_CACHE_HIT = Constant(default=0)

    PROJECT_NAME_SUPER_SLUG = Derivable(cache=True)

    @PROJECT_NAME_SUPER_SLUG.getter
    def get_PROJECT_NAME_SUPER_SLUG(self, sep):
        self.PROJECT_NAME_SUPER_SLUG_CACHE_HIT.set_value(
            self.PROJECT_NAME_SUPER_SLUG_CACHE_HIT.get_value() + 1
        )
        return self.PROJECT_NAME.get_value().replace("_", sep)

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return "{}-{}".format(
            self.PROJECT_NAME_SLUG.get_value(),
            self.STAGE.get_value(),
        )

    GIT_PASSWORD = Constant(printable=False)

    CREATE_TIME = Constant(default=datetime.utcnow)

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

    # when trying to get a derivable value but the dependent constant value
    # has not been set yet
    try:
        conf.PROJECT_NAME_SLUG.get_value()
    except Exception as e:
        assert "Config.PROJECT_NAME" in str(e)
        assert "Config.PROJECT_NAME_SLUG" in str(e)

    with raises(ValueNotSetError):
        conf.PROJECT_NAME_SLUG.get_value()

    try:
        conf.ENVIRONMENT_NAME.get_value()
    except Exception as e:
        assert "PROJECT_NAME" in str(e)
        assert "PROJECT_NAME_SLUG" in str(e)
        assert "ENVIRONMENT_NAME" in str(e)


def test_default():
    conf = Config()
    assert isinstance(conf.CREATE_TIME.get_value(), datetime)


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


def test_get_value_for_lbd():
    conf = Config(PROJECT_NAME="configirl")
    PREFIX = "CONFIGIRL_"
    assert conf.PROJECT_NAME.get_value_for_lbd(PREFIX) == "configirl"


def test_get_value_with_cache():
    config = Config(PROJECT_NAME="my_project")
    assert config.PROJECT_NAME_SUPER_SLUG.get_value(sep="--") == "my--project"
    assert config.PROJECT_NAME_SUPER_SLUG_CACHE_HIT.get_value() == 1

    assert config.PROJECT_NAME_SUPER_SLUG.get_value(sep="--") == "my--project"
    assert config.PROJECT_NAME_SUPER_SLUG_CACHE_HIT.get_value() == 1


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
