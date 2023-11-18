#!/bin/bash
pip install -r requirements.txt

# 获取脚本的路径
script_path=$(dirname "$0")

# 构建 data.txt 的相对路径
data_file_path="$script_path/main.py"

python $data_file_path