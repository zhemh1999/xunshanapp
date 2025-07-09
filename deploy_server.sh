#!/bin/bash

# 自习室管理系统 - 云服务器一键部署脚本
# 适用于: Ubuntu 18.04+ / CentOS 7+ / Debian 9+

set -e

echo "🚀 自习室管理系统 - 云服务器一键部署脚本"
echo "=================================================="

# 检查是否为root用户
if [[ $EUID -ne 0 ]]; then
   echo "❌ 请使用root用户运行此脚本"
   echo "   sudo bash deploy_server.sh"
   exit 1
fi

# 获取操作系统信息
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
fi

echo "📋 检测到操作系统: $OS $VER"

# 更新系统
echo "🔄 更新系统包..."
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    apt update && apt upgrade -y
    apt install -y python3 python3-pip nginx supervisor git curl
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
    yum update -y
    yum install -y python3 python3-pip nginx supervisor git curl epel-release
    yum install -y python3-pip
fi

# 检查Python版本
python3_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $python3_version"

# 创建应用目录
APP_DIR="/var/www/xunshanapp"
echo "📁 创建应用目录: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR

# 如果当前目录有文件，复制到应用目录
if [ -f "/root/xunshanapp/app.py" ]; then
    echo "📋 复制本地文件到应用目录..."
    cp -r /root/xunshanapp/* $APP_DIR/
elif [ -f "./app.py" ]; then
    echo "📋 检测到当前目录有应用文件"
else
    echo "❌ 未找到应用文件"
    echo "   请确保在应用目录中运行此脚本，或将文件上传到 /root/xunshanapp/"
    exit 1
fi

# 安装Python依赖
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt

# 配置Supervisor
echo "⚙️ 配置Supervisor守护进程..."
cat > /etc/supervisor/conf.d/xunshanapp.conf << 'EOF'
[program:xunshanapp]
directory=/var/www/xunshanapp
command=python3 run_production.py
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/xunshanapp.log
stderr_logfile=/var/log/xunshanapp_error.log
environment=FLASK_ENV=production
EOF

# 启动Supervisor服务
echo "🚀 启动应用服务..."
supervisorctl reread
supervisorctl update
supervisorctl start xunshanapp

# 等待应用启动
echo "⏳ 等待应用启动..."
sleep 5

# 检查应用状态
if supervisorctl status xunshanapp | grep -q "RUNNING"; then
    echo "✅ 应用启动成功"
else
    echo "❌ 应用启动失败，请检查日志："
    echo "   tail -f /var/log/xunshanapp_error.log"
    exit 1
fi

# 配置Nginx
echo "🌐 配置Nginx反向代理..."
cat > /etc/nginx/sites-available/xunshanapp << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 静态文件缓存
    location /static {
        alias /var/www/xunshanapp/static;
        expires 1d;
        add_header Cache-Control public;
    }
    
    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
}
EOF

# 启用Nginx配置
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

ln -sf /etc/nginx/sites-available/xunshanapp /etc/nginx/sites-enabled/

# 测试Nginx配置
echo "🔍 测试Nginx配置..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx配置正确"
    systemctl restart nginx
    systemctl enable nginx
else
    echo "❌ Nginx配置错误"
    exit 1
fi

# 配置防火墙
echo "🔒 配置防火墙..."
if command -v ufw &> /dev/null; then
    # Ubuntu/Debian
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
elif command -v firewall-cmd &> /dev/null; then
    # CentOS/RHEL
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --permanent --add-service=ssh
    firewall-cmd --reload
fi

# 获取服务器IP
SERVER_IP=$(curl -s ifconfig.me || curl -s ipinfo.io/ip || hostname -I | awk '{print $1}')

# 初始化数据库
echo "🗄️ 初始化数据库..."
cd $APP_DIR
python3 -c "
from app import create_app, db, init_db
app = create_app('production')
with app.app_context():
    db.create_all()
    init_db()
    print('数据库初始化完成')
"

# 部署完成
echo ""
echo "🎉 部署完成！"
echo "=================================================="
echo "📍 访问地址: http://$SERVER_IP"
echo "🔐 管理员账户: admin / admin123"
echo "👤 登记员账户: registrar / reg123"
echo ""
echo "📋 管理命令:"
echo "   重启应用: supervisorctl restart xunshanapp"
echo "   查看日志: tail -f /var/log/xunshanapp.log"
echo "   查看错误: tail -f /var/log/xunshanapp_error.log"
echo "   重启Nginx: systemctl restart nginx"
echo ""
echo "🔒 安全提醒:"
echo "   1. 请立即修改默认密码"
echo "   2. 建议配置SSL证书"
echo "   3. 定期备份数据库文件"
echo ""
echo "💡 SSL证书配置(可选):"
echo "   如果有域名，可以配置免费SSL证书:"
echo "   certbot --nginx -d yourdomain.com"
echo ""
echo "🎊 现在可以通过浏览器访问您的自习室管理系统了！" 