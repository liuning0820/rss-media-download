#!/bin/bash

# 获取脚本的路径
script_path=$(dirname "$0")

pip install -r "$script_path/requirements.txt"

data_file_path="$script_path/main.py"

python "$data_file_path"