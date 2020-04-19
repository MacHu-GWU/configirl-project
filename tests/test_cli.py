#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from configirl import read_config_value, get_config_value


def test_read_config_value():
    cwd = os.getcwd()
    if cwd.endswith("tests"):
        assert read_config_value("./config-raw.json", "PROJECT_NAME") == "config_lib"
    elif cwd.endswith("configirl-project"):
        assert read_config_value("./tests/config-raw.json", "PROJECT_NAME") == "config_lib"
    else:
        raise NotImplementedError


def test_get_config_value():
    assert get_config_value("configirl.tests.config.Config", "PROJECT_NAME") == "my_devops"
    assert get_config_value("configirl.tests.config.Config", "PROJECT_NAME_SLUG") == "my-devops"
    assert get_config_value("configirl.tests.config.Config", "STAGE") == "dev"
    assert get_config_value("configirl.tests.config.Config", "ENVIRONMENT_NAME") == "my-devops-dev"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
