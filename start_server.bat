@echo off
REM 自习室管理系统启动脚本 (Windows)

echo 正在启动自习室管理系统...

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 安装依赖
echo 正在安装依赖...
pip install -r requirements.txt

REM 设置环境变量
set FLASK_ENV=production
set PORT=8000

REM 启动服务器
echo 正在启动服务器...
python run_production.py

pause 