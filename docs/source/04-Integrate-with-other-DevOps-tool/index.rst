.. _int-with-devops-tool:

Integrate with other DevOps Tool
==============================================================================

To integrate configirl framework with other programming language, or other DevOps tool, you need a intermediate to exchange data. You have several options:

1. json file.
2. environment variable.
3. external store like AWS Parameter Store.

In this document, let's use `terraform <https://www.terraform.io/>`_, a famous Infrastructure as Code open source tool, to demonstrate the idea.

In terraform, you can define `input variables <https://www.terraform.io/docs/configuration/variables.html>`_. But it is not to write complex variable handling logic in terraform, since natively it is just a DSL (Domain Specified Language). But you can define some variables, and inject value from ``configirl`` into ``terraform``.

The integration layer is simple. You just use ``configirl`` to initialize yoru config object, then duump into the ``terraform.tfvars.json`` file, which would be the `variable input <https://www.terraform.io/docs/configuration/variables.html#variable-definitions-tfvars-files>`_ for terraform.

Code example:

config declaration:

.. literalinclude:: ../../../configirl/tests/config.py
    :language: python
    :caption: https://github.com/MacHu-GWU/configirl-project/blob/master/configirl/tests/config.py
    :linenos:

config initialization:

.. code-block:: python

    # content of config_init.py
    from .config import Config
    from configirl import write_text

    config = Config()

    write_text("/path-to-terraform-dir/terraform.tfvars.json", config.to_json())

terraform integration:

.. code-block:: bash

    python config_init.py
    terraform apply

