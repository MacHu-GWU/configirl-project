.. image:: https://readthedocs.org/projects/configirl/badge/?version=latest
    :target: https://configirl.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/configirl-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/configirl-project/actions?query=workflow:CI

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

**If you are looking for technical support**, click the badge below to join this gitter chat room and ask question to the author.

.. image:: https://img.shields.io/badge/Chat-Tech_Support-_.svg
      :target: https://gitter.im/MacHu-GWU-Python-Library-Technical-Support/community

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
