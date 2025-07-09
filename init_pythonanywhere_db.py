#!/usr/bin/env python3
"""
PythonAnywhere数据库初始化脚本
在PythonAnywhere Bash控制台中运行此脚本来初始化数据库
"""
import os
import sys

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'
os.environ['SERVER_NAME'] = 'pythonanywhere'

# 导入应用
try:
    from app import create_app, db, init_db
    print("✅ 成功导入应用模块")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保：")
    print("1. 当前目录是项目根目录")
    print("2. 已安装所有依赖：pip3.10 install --user -r requirements.txt")
    print("3. app.py文件存在且可访问")
    sys.exit(1)

def main():
    """初始化数据库"""
    print("🚀 开始初始化PythonAnywhere数据库...")
    
    # 创建应用实例
    app = create_app('production')
    
    with app.app_context():
        try:
            print("📋 创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建成功")
            
            print("👥 初始化默认用户...")
            init_db()
            print("✅ 默认用户创建成功")
            
            print("\n🎉 数据库初始化完成！")
            print("\n默认账户：")
            print("🔑 管理员：admin / admin123")
            print("👤 登记员：registrar / reg123")
            print("\n⚠️  请登录后立即修改默认密码！")
            
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            print("\n请检查：")
            print("1. MySQL数据库是否已创建")
            print("2. 数据库连接配置是否正确")
            print("3. 是否安装了PyMySQL：pip3.10 install --user PyMySQL")
            return False
    
    return True

if __name__ == "__main__":
    # 显示当前环境信息
    print("🔍 环境信息：")
    print(f"Python版本：{sys.version}")
    print(f"当前目录：{os.getcwd()}")
    print(f"FLASK_ENV：{os.environ.get('FLASK_ENV', 'Not set')}")
    print()
    
    # 执行初始化
    success = main()
    
    if success:
        print("\n✨ 初始化完成，您的自习室管理系统已就绪！")
        print("🌐 访问您的网站：http://yourusername.pythonanywhere.com")
    else:
        print("\n💔 初始化失败，请检查错误信息并重试")
        sys.exit(1) 