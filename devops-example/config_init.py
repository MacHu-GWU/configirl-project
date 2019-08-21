# -*- coding: utf-8 -*-
# content of config_init.py

"""
initialize the conifg object, it reads common config value from
00-config-shared.json file, and read environment specified value from config-raw.json
file
"""

import os, json
from config import Config

conf = Config()
path_shared_config_file = os.path.join(os.path.dirname(__file__), "00-config-shared.json")
conf.update(json.loads(open(path_shared_config_file, "rb").read().decode("utf-8")))
conf.update_from_raw_json_file()
conf.dump_python_json_config_file()
conf.dump_shell_script_json_config_file()
conf.dump_cloudformation_json_config_file()
