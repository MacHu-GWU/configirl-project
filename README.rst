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

``configirl`` is a **single script, pure python, no dependencies, python2.7, 3.4+ compatible, drop in ready** python library to help you **manage complex config value logic**. This devops solution applies to **ANY PROJECT, ANY PROGRAMMING LANGUAGE**.

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

**Devops Engineer has to deal with lots of config and parameters everyday**. Some config value are just a constant value, like a integer and a string. Some config value can be derived from other config values, sometimes event requires the context.

There are lots of Devops tools available in the community, such as:

- Shell Script for command line tool, automation
- Jenkins groovy for CI/CD
- Cloudformation for Infrastructure as Code
- Terraform for Infrastructure as Code
- ...

They all using different language and different syntax. The method of managing config value in different tools varies very much! If you have to manage a list of config values, and you are using multiple devops tools in the same project. Allow those tools talk to each other is NOT EASY at all. And the effort to manage config value in certain tools might be very difficult (like CloudFormation).

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


Use Case - Java Web App Project with AWS, Serverless, Infrastructure as Code
------------------------------------------------------------------------------

In this example, we are designing the devops solution for a complex Web App, the app logic is written in `JAVA Sprint <https://spring.io/>`_, the application code is deployed to Amazon Web Service via `Cloudformation <https://aws.amazon.com/cloudformation/>`_, lots of microservices are deployed to AWS Lambda and AWS ApiGateway with `Serverless framework <https://serverless.com/>`_, and use `CircleCI <https://circleci.com/>`_ to automate the test, build, deployment.

Suppose your ``project name`` is ``MyWebApp``, and it has multiple deployment ``stage`` ``dev``, ``test``, ``prod``, in other word, it will be deployed to three ``Environment``. And the environment name ``MyWebApp-dev/test/prod`` will be used as a prefix name almost everywhere in your Java Code, Cloudformation Code, CICD Code. And you **DONT want to manage the config value** like ``PROJECT_NAME`` and ``STAGE`` everywhere in Java Code, Cloudformation Code, CICD Code.

If you don't want to create the devops scripts manually in the following instruction, you can just copy the entire ``devops-example`` directory from https://github.com/MacHu-GWU/configirl-project/tree/master/devops-example to your local machine.


1. Centralize Your Config Definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to use ``configirl`` is to copy the ``configirl.__init__.py`` file to your Devops workspace directory, and rename it as ``configirl.py``. It is ``drop in ready`` and no dependencies, it runs any Mac or Linux Machine.

Create a ``config.py`` file next to ``configirl.py`` it is the centralized place to manage your config logic, put the following code in ``config.py``, it defines two major constant variables ``PROJECT_NAME`` and ``STAGE``, and two derivable variables ``PROJECT_NAME_SLUG`` and ``ENVIRONMENT_NAME``:

.. code-block:: python

    # -*- coding: utf-8 -*-
    # content of config.py

    import os
    from configirl import ConfigClass, Constant, Derivable


    class Config(ConfigClass):
        CONFIG_DIR = os.path.dirname(__file__)

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


2. Create the Config Data for Different Enviornment.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create three config files ``./01-config-dev.json``, ``./01-config-test.json``, ``./01-config-prod.json``, and put the following contect in corresponding files ``{"STAGE": "dev"}``, ``{"STAGE": "test"}``, ``{"STAGE": "prod"}``.

Create a config file ``./00-config-shared.json`` and put the following content ``{"PROJECT_NAME": "MyWebApp"}``.

**For different deployment stages, they may share common config values, those information goes to** ``./00-config-shared.json`` file.

**For environment dependent config values, they goes to different config files**.


.. _install:

Install
------------------------------------------------------------------------------

``configirl`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install configirl

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade configirl