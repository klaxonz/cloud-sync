# !/bin/bash

# 获取当前脚本所在的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 切换到 main.py 所在的目录
cd "${SCRIPT_DIR}/../src"

# 执行 main.py
python main.py --action upload