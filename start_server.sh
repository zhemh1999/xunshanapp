#!/bin/bash
# 自习室管理系统启动脚本

echo "正在启动自习室管理系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt

# 设置环境变量
export FLASK_ENV=production
export PORT=8000

# 启动服务器
echo "正在启动服务器..."
python3 run_production.py 