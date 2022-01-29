#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from configirl import read_json_value, get_config_value, import_config_value


def test_read_config_value():
    cwd = os.getcwd()
    if cwd.endswith("tests"):
        abspath = os.path.join(cwd, "./config-raw.json")
        assert read_json_value("./config-raw.json", "PROJECT_NAME") == "config_lib"
        assert read_json_value("./config-raw.json", "$.PROJECT_NAME") == "config_lib"
        assert read_json_value(abspath, "PROJECT_NAME") == "config_lib"
        assert read_json_value(abspath, "$.PROJECT_NAME") == "config_lib"

        with pytest.raises(ValueError):
            read_json_value(abspath, "$.PROJECT_NAME.NOT_EXIST_FIELD")
    elif cwd.endswith("configirl-project"):
        assert read_json_value("./tests/config-raw.json", "PROJECT_NAME") == "config_lib"
    else:
        raise NotImplementedError


def test_get_config_value():
    assert get_config_value("configirl.tests.config.Config", "PROJECT_NAME") == "my_devops"
    assert get_config_value("configirl.tests.config.Config", "PROJECT_NAME_SLUG") == "my-devops"
    assert get_config_value("configirl.tests.config.Config", "STAGE") == "dev"
    assert get_config_value("configirl.tests.config.Config", "ENVIRONMENT_NAME") == "my-devops-dev"
    assert get_config_value("configirl.tests.config.Config", "is_prod_runtime") is False
    assert get_config_value("configirl.tests.config.Config", "_version") == "0.0.1"


def test_import_config_value():
    sys_path = os.path.dirname(os.path.dirname(__file__))  # configirl-project
    assert import_config_value(
        sys_path=sys_path,
        module="configirl.tests.config.Config",
        field="ENVIRONMENT_NAME",
    ) == "my-devops-dev"

    assert import_config_value(
        sys_path=os.path.join(sys_path, "configirl", "tests"),
        module="config.Config",
        field="ENVIRONMENT_NAME",
    ) == "my-devops-dev"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
