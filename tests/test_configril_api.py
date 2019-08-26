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

    # specify dont_dump to avoid dump to dict or json
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

    def test_dont_dump_with_json_incompatible_value(self):
        conf = Config(PROJECT_NAME="my_project", STAGE="dev")
        conf.to_json() # PARAM_ENV_NAME doesn't cause any problem

    def test_update_from_env_var(self):
        environ["MY_APP_PROJECT_NAME"] = "my_project"
        conf = Config(PROJECT_NAME="other_project")
        conf.update_from_env_var(prefix="MY_APP_")
        assert conf.PROJECT_NAME.get_value() == "my_project"
        with pytest.raises(ValueNotSetError):
            conf.STAGE.get_value()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
