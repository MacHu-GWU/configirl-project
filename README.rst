.. image:: https://readthedocs.org/projects/configirl/badge/?version=latest
    :target: https://configirl.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://travis-ci.org/MacHu-GWU/configirl-project.svg?branch=master
    :target: https://travis-ci.org/MacHu-GWU/configirl-project?branch=master

.. image:: https://codecov.io/gh/MacHu-GWU/configirl-project/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/MacHu-GWU/configirl-project

.. image:: https://img.shields.io/pypi/v/configirl.svg
    :target: https://pypi.python.org/pypi/configirl

.. image:: https://img.shields.io/pypi/l/configirl.svg
    :target: https://pypi.python.org/pypi/configirl

.. image:: https://img.shields.io/pypi/pyversions/configirl.svg
    :target: https://pypi.python.org/pypi/configirl

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/configirl-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
      :target: https://configirl.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
      :target: https://configirl.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
      :target: https://configirl.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
      :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
      :target: https://github.com/MacHu-GWU/configirl-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
      :target: https://github.com/MacHu-GWU/configirl-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
      :target: https://github.com/MacHu-GWU/configirl-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
      :target: https://pypi.org/pypi/configirl#files


Welcome to ``configirl`` Documentation
==============================================================================

.. contents::
    :depth: 1
    :local:


What is ``configirl``
------------------------------------------------------------------------------

``configirl`` is a **single script, pure python, no dependencies, python2.7, 3.4+ compatible, drop in ready** python library to help you **manage complex config value logic**.

.. code-block:: python

    from configirl import ConfigClass, Constant, Deriable

    class Config(object):
        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Deriable()

        @PROJECT_NAME_SLUG.getter
        def get_project_name_slug(self):
            return self.PROJECT_NAME.get_value().replace("_", "-")

    config = Config(PROJECT_NAME="my_project")


What problem does ``configirl`` solve
------------------------------------------------------------------------------

Devops Engineer has to deal with lots of config and parameters everyday. Some config value are just a constant value, like a integer and a string. Some config value can be derived from other config values, sometimes event requires the context.

There are lots of Devops tools available in the community, such as:

- Shell Script for command line tool, automation
- Jenkins groovy for CI/CD
- Cloudformation for Infrastructure as Code
- Terraform for Infrastructure as Code
- ...

They all using different language and different syntax. The way, and flexibility of managing config value in different tools varies very much! If you have to manage a list of config values, and you are using multiple devops tools in the same project. Allow those tools talk to each other is NOT EASY at all. And the effort to manage config value in certain tools might be very difficult (like CloudFormation).

``configirl`` **provides a solution to manage complex logic for config values in an elegant way. Since Python is easy to learn and it is full featured programming language, you got the perfect balance of simplicity and flexibility**. To integrate with any Devops tools, you just reference the value from the finalized config JSON file.


Quick Start
------------------------------------------------------------------------------

1. Copy ``configirl.__init__.py`` to your Devops workspace directory, and rename it as ``configirl.py``. That is for ``drop in ready``.
2. Create a ``config-raw.json`` file put the following content:

.. code-block:: javascript

    {
        "PROJECT_NAME": "my_project",
        "STAGE": "dev"
    }

3. Create a ``config.py`` file, put the following content. Since it is Python2.7, 3.4+ compatible, pure Python, no dependencies, it works everywhere.

.. code-block:: python

    from configirl import ConfigClass, Constant, Derivable

    class Config(object):
        CONFIG_DIR = "your-devops-workspace-dir"

        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Derivable()

        @PROJECT_NAME_SLUG.getter
        def get_project_name_slug(self):
            return self.PROJECT_NAME.get_value().replace("_", "-")

        @PROJECT_NAME_SLUG.validator
        def check_project_name_slug(self, value):
            if "_" in value:
                raise ValueError("you can't use `_` in slugifie name!")

        STAGE = Constant()

        ENVIRONMENT_NAME = Derivable()

        @PROJECT_NAME_SLUG.getter
        def get_environment_name(self):
            return "{}-{}".format(
                self.PROJECT_NAME_SLUG.get_value(),
                self.STAGE.get_value(),
            )

    config = Config()
    config.update_from_raw_json_file()
    config.dump_shell_script_json_config_file()
    config.dump_cloudformation_json_config_file()
    # you can call more custom dump method here
    # depends on what other devops tools you are using

4. Everytime you call ``python config.py`` then the ground truth config value in ``config-raw.json`` will be parsed. and two more ``config-final-for-shell-script.json``, ``config-final-for-cloudformation.json`` will be create. Then you can just reference value from thos ``xxx-final-xxx.json`` file.

.. code-block:: javascript

    // content of config-final-for-shell-script.json
    {
        "PROJECT_NAME": "my_project",
        "PROJECT_NAME_SLUG": "my-project",
        "STAGE": "dev",
        "ENVIRONMENT_NAME": "my-project-dev"
    }

.. code-block:: javascript

    // content of config-final-for-cloudformation.json
    {
        "ProjectName": "my_project",
        "ProjectNameSlug": "my-project",
        "Stage": "dev",
        "EnvironmentName": "my-project-dev"
    }


Additional Feature
------------------------------------------------------------------------------

1. you can custom your validator.

.. code-block:: python

    from configirl import ConfigClass, Constant, Derivable

    class Config(object):
        PROJECT_NAME = Constant()
        PROJECT_NAME_SLUG = Derivable()

        @PROJECT_NAME_SLUG.getter
        def get_project_name_slug(self):
            return self.PROJECT_NAME.get_value().replace("_", "-")

        @PROJECT_NAME_SLUG.validator
        def check_project_name_slug(self, value):
            if "_" in value:
                raise ValueError("you can't use `_` in slugifie name!")

2. you can inherit your Config Class.

.. code-block:: python

    from configirl import ConfigClass, Constant, Derivable

    class Config1(object):
        PROJECT_NAME = Constant()

    class Config2(Config1):
        PROJECT_NAME_SLUG = Derivable()

        @PROJECT_NAME_SLUG.getter
        def get_project_name_slug(self):
            return self.PROJECT_NAME.get_value().replace("_", "-")

        @PROJECT_NAME_SLUG.validator
        def check_project_name_slug(self, value):
            if "_" in value:
                raise ValueError("you can't use `_` in slugifie name!")

    class Config(Config2):
        CONFIG_DIR = "your-devops-workspace-dir"

    config = Config()
    ... do what every you need


.. _install:

Install
------------------------------------------------------------------------------

``configirl`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install configirl

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade configirl