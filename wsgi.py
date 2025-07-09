#!/usr/bin/env python3
"""
WSGI配置文件 - 用于生产环境部署
支持gunicorn、uWSGI等WSGI服务器
"""
import os
from app import create_app

# 获取环境变量，默认为生产环境
config_name = os.environ.get('FLASK_ENV') or 'production'

# 创建应用实例
app = create_app(config_name)

if __name__ == "__main__":
    # 如果直接运行此文件，启动开发服务器
    app.run(debug=False, host='0.0.0.0', port=5000) 