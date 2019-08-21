# -*- coding: utf-8 -*-

import pytest
from os import environ, path
from configirl import (
    ConfigClass, Constant, Derivable, ValueNotSetError
)


class Parameter(object):
    def __init__(self, value):
        self.value = value


class Config(ConfigClass):
    CONFIG_DIR = path.dirname(__file__)

    PROJECT_NAME = Constant()
    STAGE = Constant()

    PARAM_ENV_NAME = Derivable(dont_dump=True)

    @PARAM_ENV_NAME.getter
    def get_PARAM_ENV_NAME(self):
        return Parameter("{}-{}".format(
            self.PROJECT_NAME.get_value().replace("_", "-"),
            self.STAGE.get_value(),
        ))


class TestConfig(object):
    def test_value_not_set_error(self):
        conf = Config(non_related_var=None)
        with pytest.raises(ValueNotSetError):
            conf.to_dict()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
