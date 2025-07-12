#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from app import create_app, init_db, db

def main():
    print("=" * 60)
    print("🏫 自习室管理系统启动中...")
    print("=" * 60)
    
    try:
        # 创建应用实例
        app = create_app('development')
        
        # 在应用上下文中初始化数据库
        with app.app_context():
            print("📁 正在初始化数据库...")
            db.create_all()
            init_db()
        
        print("\n✅ 系统启动成功！")
        print("=" * 60)
        print("🌐 访问地址:")
        print("   - http://127.0.0.1:5000")
        print("   - http://localhost:5000")
        print("\n🔐 默认账户:")
        print("   管理员: admin / admin123")
        print("   登记员: registrar / reg123")
        print("\n💡 功能说明:")
        print("   - 管理39个座位 (A01-A30, B01-B09)")
        print("   - 座位信息管理 (姓名、卡类型、到期时间、起始时间、好评、电话)")
        print("   - 操作记录查看 (仅管理员)")
        print("   - 数据统计和筛选")
        print("=" * 60)
        print("📱 Android版本：参见 android_config.md")
        print("📖 使用说明：参见 README.md")
        print("=" * 60)
        print("⚠️  按 Ctrl+C 可以停止服务器")
        print("=" * 60)
        
        # 启动Flask应用
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 系统已关闭")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 