# -*- coding: utf-8 -*-

import pytest
from configirl import (
    ConfigClass, Constant, Derivable,
)


class Config(ConfigClass):
    pass


def test_detect_environment():
    Config.is_aws_ec2_amz_linux_runtime()
    Config.is_aws_lambda_runtime()
    Config.is_aws_code_build_runtime()
    Config.is_ci_runtime()
    Config.is_circle_ci_runtime()
    Config.is_travis_ci_runtime()
    Config.is_gitlab_ci_runtime()


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
