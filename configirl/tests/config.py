# -*- coding: utf-8 -*-

from configirl import ConfigClass, Constant, Derivable


class Config(ConfigClass):
    PROJECT_NAME = Constant(default="my_devops")
    PROJECT_NAME_SLUG = Derivable()

    @PROJECT_NAME_SLUG.getter
    def get_PROJECT_NAME_SLUG(self):
        return self.PROJECT_NAME_SLUG.get_value().replace("_", "-")

    STAGE = Constant(default="dev")

    ENVIRONMENT_NAME = Derivable()

    @ENVIRONMENT_NAME.getter
    def get_ENVIRONMENT_NAME(self):
        return "{}-{}".format(self.PROJECT_NAME_SLUG.get_value(), self.STAGE.get_value())
