# -*- coding: utf-8 -*-
# content of config_init.py

"""
initialize the config object, it reads common config value from the
``00-config-shared.json`` file, and read environment specified value from the
``config-raw.json`` file.

Suppose that:

- on local development, you load all values from your local file.
- on CI/CD environment, you load non-sensitive values from Git repo, load
    sensitive values from AWS Secret Manager. Because you don't 100% trust your
    CI/CD provider.
- on EC2 App server, you load non-sensitive values from Git repo, load 
    sensitive values from Environment Variable. Because the servers locates 
    at secure environment.
"""

import os, json
from config import Config

conf = Config()

path_shared_config_file = os.path.join(os.path.dirname(__file__), "00-config-shared.json")
path_shared_secrets_config_file = os.path.join(os.path.dirname(__file__), "00-config-shared-secrets.json")


# load non sensitive values
conf.update(json.loads(open(path_shared_config_file, "rb").read().decode("utf-8")))

# load environment specified values
conf.update_from_raw_json_file() # load environment specific values

# load sensitive values
if conf.is_aws_ec2_runtime():
    conf.update_from_env_var(prefix="APP_CONFIG_")
elif conf.is_ci_runtime():
    def read_sensitive_value_from_aws_secret_manager():
        return dict()
    conf.update(read_sensitive_value_from_aws_secret_manager())
else:
    conf.update(json.loads(open(path_shared_secrets_config_file, "rb").read().decode("utf-8")))

# dump other derivable values for other system to use
if conf.is_ci_runtime(): # allow other system like terraform to use those value for deployment
    conf.dump_shell_script_json_config_file()
    conf.dump_terraform_json_config_file()

