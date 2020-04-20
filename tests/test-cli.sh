#!/bin/bash
# -*- coding: utf-8 -*-

dir_here="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_here}")"
source "${dir_project_root}/bin/py/python-env.sh"

v="$(${dir_venv_bin}/configirl read-json-value --path ${dir_project_root}/tests/config-raw.json --field "PROJECT_NAME")"
echo $v
if [ "${v}" != "config_lib" ]; then
    echo "configirl read-json-value failed!"
    exit 1
fi

v="$(${dir_venv_bin}/configirl get-config-value --module configirl.tests.config.Config --field "ENVIRONMENT_NAME")"
echo $v
if [ "${v}" != "my-devops-dev" ]; then
    echo "configirl get-config-value failed!"
    exit 1
fi

v="$(${dir_venv_bin}/configirl get-config-value --module configirl.tests.config.Config --field "is_prod_runtime")"
echo $v
if [ "${v}" != "False" ]; then
    echo "configirl import-config-value failed!"
    exit 1
fi

v="$(${dir_venv_bin}/configirl get-config-value --module configirl.tests.config.Config --field "__module__")"
echo $v
if [ "${v}" != "configirl.tests.config" ]; then
    echo "configirl import-config-value failed!"
    exit 1
fi

v="$(${dir_venv_bin}/configirl import-config-value --sys_path ${dir_project_root}/configirl --module tests.config.Config --field "ENVIRONMENT_NAME")"
echo $v
if [ "${v}" != "my-devops-dev" ]; then
    echo "configirl import-config-value failed!"
    exit 1
fi
