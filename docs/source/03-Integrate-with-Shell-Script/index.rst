.. _int-with-shell-script:

Integrate with Shell Script
==============================================================================

.. contents::
    :depth: 1
    :local:

Writing complex conditional logic in shell script is painful, and hard to maintain. That was one of the motivation I create ``configirl``. **So having** ``configirl`` **to manage complex multi-environment dynamic configuration, how could we reference config values in shell script?**

First, let's imaging a standard **use case**:

    You have a shell scripts that deploying a web app to AWS. There are some aws cli commands.

    - On your local computer, basically it is called ``dev`` environment. You use an IAM User AWS_PROFILE. so in all of your aws command line, you need to pass ``--profile my_aws_profile`` arg.
    - But in your CI/CD environment (let's say circleci), basically it is ``test`` environment, and after passing the integration test, you deploy it to ``prod`` environment. In this case, you use AWS credential from environment variable. So you don't need to pass ``--profile`` arg.

    You don't want to maintain three different shell scripts for dev, test, prod. Ideally you only want one deployment script and works everywhere, and automatically referencing dynamic configs and perform similar deployment automation.

**Here's the solution with configirl**:

1. You can **create a json config file to store non sensitive data for your local development**, such as AWS_PROFILE. Please be aware of where you store it.

.. code-block:: javascript

    // content of $HOME/my-project/config/config.json
    {
        "AWS_PROFILE": "my_aws_profile"
    }

2. You use ``configirl`` to **declare a python file for dynamic config values**.

.. code-block:: python

    # content of $HOME/my-project/config/config.py
    import json
    from configirl import ConfigClass, Constant, Derivable

    class Config(ConfigClass):
        STAGE = Constant()

        AWS_PROFILE = Derivable()

        @AWS_PROFILE.getter
        def get_AWS_PROFILE():
            # custom runtime detection function
            if self.is_aws_ec2_amz_linux_runtime():
                return None
            # custom runtime detection function
            elif self.is_circle_ci_runtime():
                return None
            else: # local runtime
                with open("~/my-project/config/config.json", "r") as f:
                    return json.loads(f.read())["AWS_PROFILE"]

        AWS_CLI_PROFILE_ARG = Derivable()

        @AWS_CLI_PROFILE_ARG.getter
        def get_AWS_CLI_PROFILE_ARG(self):
            if self.is_aws_ec2_amz_linux_runtime():
                return ""
            elif self.is_circle_ci_runtime():
                return ""
            else: # local runtime
                return "--profile {}".format(self.AWS_PROFILE.get_value())

3. Write you shell script tool ``deploy.sh`` that deploy app to specific environment. You use configirl cli to retrieve dynamic config value ``AWS_CLI_PROFILE_ARG``. On local, it is ``--profile my_aws_profile``. On other runtime, it is empty string. As a result, your shell scripts works everywhere and behave differently in different environment. For detailed document for cli interface, see :ref:`configirl-cli`.

.. code-block:: bash

    #/bin/bash
    # content of deploy.sh
    #
    # usage:
    #
    #   $ bash deploy.sh dev
    #   $ bash deploy.sh test
    #   $ bash deploy.sh prod

    stage="$1"
    bash ./switch-env ${stage}

    aws_cli_profile_arg="$(configirl import-config-value --sys_path ${HOME}/my-project/config --module config.Config --field AWS_CLI_PROFILE_ARG)"

    # deployment your web app to AWS
    aws cloudformation ... "${aws_cli_profile_arg}"

Now you have a utility tool easily load dynamic configuration and deploy web app to different environment as you wish.

4. Wrap up your CI/CD automation script.

.. code-block:: bash

    #/bin/bash
    # content of cicd.sh
    #
    # usage:
    #
    #   $ bash cicd.sh

    bash deploy.sh test # deploy to test
    bash run-integration-test.sh # run integration test on test environment
    bash deploy.sh prod # deploy to production
