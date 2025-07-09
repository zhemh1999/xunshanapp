#!/usr/bin/env python3
"""
PythonAnywhere WSGI配置文件
使用此文件作为PythonAnywhere Web应用的WSGI配置
"""
import sys
import os

# 添加项目路径到Python路径
# 注意：将 'yourusername' 替换为您的PythonAnywhere用户名
project_home = '/home/yourusername/xunshanapp'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'
os.environ['SERVER_NAME'] = 'pythonanywhere'

# 导入应用
try:
    from app import create_app
    application = create_app('production')
except ImportError as e:
    # 如果导入失败，创建一个简单的WSGI应用来显示错误
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/html; charset=utf-8')]
        start_response(status, headers)
        return [f"""
        <html>
        <head><title>导入错误</title></head>
        <body>
        <h1>应用导入失败</h1>
        <p>错误信息：{str(e)}</p>
        <p>请检查：</p>
        <ul>
        <li>确保所有依赖已安装：pip3.10 install --user -r requirements.txt</li>
        <li>检查项目路径是否正确：{project_home}</li>
        <li>确认app.py文件存在并可访问</li>
        </ul>
        </body>
        </html>
        """.encode('utf-8')]

if __name__ == "__main__":
    # 本地测试时运行
    application.run(debug=False, host='0.0.0.0', port=5000) 