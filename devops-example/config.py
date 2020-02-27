# -*- coding: utf-8 -*-
# content of config.py

"""
defines the constant and derivable config value.
"""

import os
from configirl import ConfigClass, Constant, Derivable


class Config(ConfigClass):
    CONFIG_DIR = os.path.dirname(__file__) # config stores at the ``devops-example`` directory

    PROJECT_NAME = Constant()  # example "MyWebApp"
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_PROJECT_NAME_SLUG(self):
        return self.PROJECT_NAME.get_value().replace("_", "-")

    @PROJECT_NAME_SLUG.validator
    def check_PROJECT_NAME_SLUG(self, value):
        if "_" in value:
            raise ValueError("you can't use `_` in slugifie name!")

    STAGE = Constant()  # example "dev"

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return "{}-{}".format(
            self.PROJECT_NAME_SLUG.get_value(),
            self.STAGE.get_value(),
        )

    APP_PUBLIC_URL = Derivable()
    @APP_PUBLIC_URL.getter
    def get_APP_PUBLIC_URL(self):
        return "https://www.{}.com/{}".format(
            self.PROJECT_NAME.get_value().lower(),
            self.STAGE.get_value(),
        )

    GITHUB_ACCESS_TOKEN = Constant(dont_dump=True, printable=False) # sensitive config value
