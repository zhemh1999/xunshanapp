# 🚀 ngrok 快速外网部署（5分钟完成）

## 🎯 目标
最快速度实现外网访问，让其他人可以通过网页链接访问您的自习室管理系统。

## 📋 准备工作
- 确保您的应用可以本地运行
- 需要稳定的网络连接

## 🔧 步骤1：下载ngrok

1. **访问官网**：https://ngrok.com/
2. **注册账户**（免费）
3. **下载ngrok**：选择您的操作系统版本
4. **解压文件**：将ngrok.exe放到您的项目目录

## 🚀 步骤2：获取认证令牌

1. **登录ngrok控制台**
2. **复制认证令牌**（形如：`1a2b3c4d...`）
3. **配置认证**：
   ```bash
   ngrok authtoken 您的认证令牌
   ```

## 🌐 步骤3：启动应用

1. **启动您的应用**：
   ```bash
   python run_production.py
   ```
   确保看到："访问地址: http://0.0.0.0:8000"

2. **新开终端窗口**，运行ngrok：
   ```bash
   ngrok http 8000
   ```

## 🎉 步骤4：获取外网地址

ngrok启动后会显示：
```
Session Status                online
Account                      您的用户名 (Plan: Free)
Version                      3.0.0
Region                       United States (us)
Web Interface                http://127.0.0.1:4040
Forwarding                   https://abc123.ngrok.io -> http://localhost:8000
Forwarding                   http://abc123.ngrok.io -> http://localhost:8000
```

**您的外网地址就是：`https://abc123.ngrok.io`**

## 📱 测试访问

1. **本地测试**：打开浏览器，访问 `https://abc123.ngrok.io`
2. **外网测试**：将链接发给朋友，让他们测试访问
3. **手机测试**：用手机浏览器访问该链接

## 🔧 高级功能

### 自定义域名（付费功能）
```bash
ngrok http --domain=您的域名.ngrok.io 8000
```

### 基本认证
```bash
ngrok http --basic-auth "用户名:密码" 8000
```

### 查看访问日志
打开：http://localhost:4040

## 📋 完整使用脚本

创建 `start_ngrok.bat`（Windows）：
```batch
@echo off
echo 启动自习室管理系统...
start cmd /k "python run_production.py"
timeout /t 3
echo 启动ngrok隧道...
ngrok http 8000
```

创建 `start_ngrok.sh`（Linux/Mac）：
```bash
#!/bin/bash
echo "启动自习室管理系统..."
python run_production.py &
sleep 3
echo "启动ngrok隧道..."
ngrok http 8000
```

## ⚠️ 注意事项

1. **免费版限制**：
   - 随机域名（每次重启都会变）
   - 有连接数限制
   - 会话时间限制

2. **需要保持运行**：
   - 您的电脑必须保持开启
   - 应用和ngrok都必须保持运行

3. **网络稳定性**：
   - 需要稳定的网络连接
   - 断网会导致服务中断

## 💰 升级建议

**如果需要稳定服务，建议：**
1. 购买ngrok付费版（固定域名）
2. 或使用云服务器部署
3. 或使用免费的Railway等云平台

## 🆘 常见问题

**Q: 显示"连接失败"？**
A: 检查您的应用是否正在运行在8000端口

**Q: 每次重启地址都变？**
A: 免费版是随机域名，付费版可以固定域名

**Q: 访问速度慢？**
A: 免费版服务器在国外，可能会慢一些

**Q: 如何停止服务？**
A: 在ngrok窗口按Ctrl+C，然后停止您的应用

## 🎉 成功！

如果一切正常，您现在就有了一个外网可访问的自习室管理系统！

**分享您的链接：**
- 发送给同事：`https://abc123.ngrok.io`
- 贴在公告板：扫码访问
- 发到工作群：点击即可使用

---

**记住：保持您的电脑和应用运行，外网访问就会一直可用！** 