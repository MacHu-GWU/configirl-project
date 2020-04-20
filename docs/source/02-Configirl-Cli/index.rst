.. _configirl-cli:

configirl CLI
==============================================================================

.. contents::
    :depth: 1
    :local:

``configirl`` ships with built-in command line interface allows developer to easily integrate Python declartion config file with Shell Script or Command Line interface.

You can type these commands to get help info for you:

.. code-block:: bash

    $ configirl -h
    $ configirl read-json-value -h
    $ configirl get-config-value -h
    $ configirl import-config-value -h

``read-json-value`` sub command
------------------------------------------------------------------------------

Example:

.. code-block:: bash

    $ PROJECT_NAME="$(configirl read-json-value --path tests/config-final-for-python.json --field PROJECT_NAME)"

is equivalent to:

.. code-block:: bash

    $ PROJECT_NAME="$(cat tests/config-final-for-python.json | jq '.PROJECT_NAME' -r)"

And it also supports json_path with dot notation.

However, configirl can **read JSON file WITH COMMENTS like**:

.. code-block:: javascript

    // some comments
    {
        "PROJECT_NAME": "my_project" // some comments
    }

``get-config-value`` sub command
------------------------------------------------------------------------------

``configirl get-config-value`` allows you to import a config declaration python module, construct a new config object and returns the value in specific field. The common usage is to reference the return value of a custom python function. Note, the module has to be importable in your current environment.

Example:

The python declaration file:

.. literalinclude:: ../../../configirl/tests/config.py
    :language: python
    :caption: https://github.com/MacHu-GWU/configirl-project/blob/master/configirl/tests/config.py
    :linenos:

Invoke the command:

.. code-block:: bash

    $ ENVIRONMENT_NAME="$(configirl read-json-value --path tests/config-final-for-python.json --field PROJECT_NAME)"
    get-config-value --module configirl.tests.config.Config --field "ENVIRONMENT_NAME"

This command is equivalent to:

.. code-block:: python

    # -*- coding: utf-8 -*-
    # content of test.py

    from configirl.tests.config import Config

    config = Config()
    print(config.ENVIRONMENT_NAME.get_value())

.. code-block:: bash

    $ ENVIRONMENT_NAME="$(python test.py)"


``import-config-value`` sub command
------------------------------------------------------------------------------

``configirl import-config-value`` is similar to ``get-config-value``. The only difference is that it doesn't requires to be able to import globally. You can spe

allows you to import a config declaration python module, construct a new config object and returns the value in specific field. The common usage is to reference the return value of a custom python function. Note, the module has to be importable in your current environment.

Example:

The python declaration file:

.. literalinclude:: ../../../configirl/tests/config.py
    :language: python
    :caption: https://github.com/MacHu-GWU/configirl-project/blob/master/configirl/tests/config.py
    :linenos:

Invoke the command:

.. code-block:: bash

    $ ENVIRONMENT_NAME="$(configirl import-config-value --sys_path /path-to/configirl-project --module configirl.tests.config.Config --field "ENVIRONMENT_NAME")"
