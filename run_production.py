#!/usr/bin/env python3
"""
生产环境启动脚本
"""
import os
import sys
from app import create_app, db, init_db

def main():
    """主函数"""
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'production'
    
    # 创建应用实例
    app = create_app('production')
    
    # 初始化数据库
    with app.app_context():
        print("正在初始化数据库...")
        db.create_all()
        init_db()
        print("数据库初始化完成！")
    
    # 获取端口号，支持云平台环境变量
    port = int(os.environ.get('PORT', 8000))
    
    # 确保端口绑定到0.0.0.0，供外部访问
    host = '0.0.0.0'
    
    # 启动生产服务器
    print("正在启动生产服务器...")
    print(f"访问地址: http://0.0.0.0:{port}")
    print("默认管理员: admin / admin123")
    print("默认登记员: registrar / reg123")
    print("按 Ctrl+C 停止服务器")
    
    try:
        # 使用gunicorn启动
        from gunicorn.app.wsgiapp import WSGIApplication
        
        # 配置gunicorn
        sys.argv = [
            'gunicorn',
            '--bind', f'{host}:{port}',
            '--workers', '2',
            '--worker-class', 'sync',
            '--timeout', '120',
            '--keepalive', '5',
            '--max-requests', '1000',
            '--max-requests-jitter', '100',
            '--preload',
            'wsgi:app'
        ]
        
        WSGIApplication().run()
        
    except ImportError:
        print("未安装gunicorn，使用Flask开发服务器...")
        app.run(debug=False, host=host, port=port)

if __name__ == '__main__':
    main() 