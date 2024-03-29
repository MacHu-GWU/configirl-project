.. _release_history:

Release and Version History
==============================================================================


1.0.2 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.1 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- add type hint
- add aws chalice dumper


0.0.10 (2020-04-19)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add configirl cli interface for shell script integration
- add read-json-value get-config-value import-config-value command


0.0.9 (2020-03-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Derivable(..., cache=True)`` option to allow cache derived value

**Minor Improvements**

**Bugfixes**

**Miscellaneous**

- refactor ``Field.get_value`` method.

0.0.8 (2020-02-27)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Minor Improvements**

- remove ``.is_aws_ec2_runtime()`` method, add ``is_aws_ec2_amz_linux_runtime``, ``is_aws_ec2_redhat_runtime``, ``is_aws_ec2_freebsd_runtime`` methods.

**Bugfixes**

- fix type hint

**Miscellaneous**

- update The devops best practice example


0.0.7 (2019-12-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Bugfixes**

- fix bug that unable to detect CI runtime


0.0.6 (2019-09-09)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Config.get_value_for_lbd(prefix)`` method

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.5 (2019-08-25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``Config.update_from_env_var(prefix)`` method

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.4 (2019-08-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``ignore_na`` arg for ``Config.to_dict()`` method.
- add ``prefix`` arg for ``Config.to_dict()`` method.
- enrich error information when encounter ``ValueNotSetError``.
- add lots of detect runtime class method.
- add ``Field.get_value_from_env(prefix)`` method to allow you to get value from environment variables.

**Minor Improvements**

- add use case document.

**Bugfixes**

**Miscellaneous**


0.0.3 (2019-07-06)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- ``json_dumps(...)`` remains the order of the keys.
- ``to_cloudformation_config_data(...)`` use OrderedDict rather than dict

**Miscellaneous**

- more docs


0.0.2 (2019-07-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

Better Document


0.0.1 (2019-07-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- First release