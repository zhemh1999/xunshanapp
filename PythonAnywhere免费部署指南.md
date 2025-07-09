# 🚀 PythonAnywhere 免费部署指南（真正零成本！）

## 🎯 为什么选择PythonAnywhere？

**真正免费 + 无需信用卡 + 专为Python设计！**

- ✅ **真正免费**：Beginner计划永久免费
- ✅ **无需信用卡**：注册即可使用，无隐藏费用
- ✅ **专为Python**：完美支持Flask应用
- ✅ **包含数据库**：免费MySQL 500MB
- ✅ **不会休眠**：24/7在线，无休眠机制
- ✅ **简单易用**：Web界面管理，无需命令行

**与其他平台对比：**
- Railway：$5/月，需要信用卡
- Render：需要信用卡验证
- Fly.io：需要信用卡
- **PythonAnywhere：完全免费，无需信用卡！** ⭐

---

## 📋 免费版限制说明

**PythonAnywhere免费版包含：**
- ✅ **1个Web应用**：完全够用
- ✅ **500MB存储空间**：足够小型应用
- ✅ **1个MySQL数据库500MB**：足够存储座位数据
- ✅ **100秒/天CPU时间**：轻量级应用完全够用
- ✅ **自定义域名支持**：yourname.pythonanywhere.com

**实际使用评估：**
- 自习室管理系统：每次操作约0.1秒CPU
- 每天100次操作 = 10秒CPU使用
- **完全在免费限制范围内！** ✅

---

## 🚀 部署步骤详解

### 步骤1：注册PythonAnywhere账户

1. **访问官网**：
   ```
   https://www.pythonanywhere.com
   ```

2. **点击注册**：
   - 点击右上角 "Pricing & signup"
   - 选择 **"Create a Beginner account"**（免费）

3. **填写注册信息**：
   ```
   Username: 您的用户名（这将成为域名的一部分）
   Email: 您的邮箱
   Password: 设置密码
   ```
   **重要**：用户名将决定您的网站地址：`http://您的用户名.pythonanywhere.com`

4. **验证邮箱**：
   - 检查邮箱收到的验证链接
   - 点击验证完成注册

### 步骤2：上传代码文件

1. **登录PythonAnywhere**：使用刚注册的账户登录

2. **进入Files页面**：
   - 点击顶部导航栏的 "Files"
   - 这里是文件管理界面

3. **创建项目目录**：
   - 在 `/home/您的用户名/` 目录下
   - 点击 "New directory"
   - 创建文件夹：`xunshanapp`

4. **上传代码文件**：
   
   **方法1：网页上传（推荐）**
   ```
   1. 进入 xunshanapp 文件夹
   2. 点击 "Upload a file"
   3. 选择以下关键文件上传：
      - app.py
      - requirements.txt
      - run_production.py
      - config.py
      - wsgi.py
      - templates/ 文件夹（所有HTML文件）
   ```

   **方法2：Git克隆**
   ```bash
   # 在PythonAnywhere的Bash控制台中执行
   cd ~
   git clone https://github.com/zhemh1999/xunshanapp.git
   ```

### 步骤3：安装依赖包

1. **打开Bash控制台**：
   - 点击顶部 "Consoles"
   - 选择 "Bash"

2. **进入项目目录**：
   ```bash
   cd ~/xunshanapp
   ```

3. **安装依赖**：
   ```bash
   pip3.10 install --user -r requirements.txt
   ```

### 步骤4：创建和配置数据库

1. **进入Databases页面**：
   - 点击顶部导航 "Databases"

2. **创建MySQL数据库**：
   ```
   Database name: xunshanapp$default
   ```
   （PythonAnywhere会自动添加您的用户名前缀）

3. **记录数据库信息**：
   ```
   Host: 您的用户名.mysql.pythonanywhere-services.com
   Database: 您的用户名$default
   Username: 您的用户名
   Password: 您设置的数据库密码
   ```

### 步骤5：配置Web应用

1. **进入Web页面**：
   - 点击顶部导航 "Web"

2. **创建新的Web应用**：
   - 点击 "Add a new web app"
   - 选择域名：`您的用户名.pythonanywhere.com`
   - Python版本：**Python 3.10**
   - 框架：**Manual configuration**

3. **配置WSGI文件**：
   - 找到 "Code" 部分
   - 点击 WSGI 配置文件链接
   - 编辑内容为：

```python
import sys
import os

# 添加项目路径
project_home = '/home/您的用户名/xunshanapp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'

# 导入应用
from app import create_app
application = create_app('production')
```

4. **配置虚拟环境**（可选）：
   - 在 "Virtualenv" 部分
   - 输入：`/home/您的用户名/.local`

5. **配置静态文件**：
   - URL: `/static/`
   - Directory: `/home/您的用户名/xunshanapp/static/`

### 步骤6：修改数据库配置

需要修改配置以使用MySQL：

1. **编辑config.py**：
   在PythonAnywhere的文件编辑器中修改：

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # MySQL数据库配置（PythonAnywhere）
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '您的用户名.mysql.pythonanywhere-services.com'
    MYSQL_USER = os.environ.get('MYSQL_USER') or '您的用户名'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '您的数据库密码'
    MYSQL_DB = os.environ.get('MYSQL_DB') or '您的用户名$default'
    
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}
```

2. **安装MySQL支持**：
   ```bash
   pip3.10 install --user PyMySQL
   ```

### 步骤7：初始化数据库

1. **在Bash控制台中执行**：
   ```bash
   cd ~/xunshanapp
   python3.10 -c "
   from app import create_app, db, init_db
   app = create_app('production')
   with app.app_context():
       db.create_all()
       init_db()
       print('数据库初始化完成')
   "
   ```

### 步骤8：启动Web应用

1. **回到Web页面**
2. **点击绿色的 "Reload" 按钮**
3. **等待重新加载完成**

---

## 🎉 测试访问

### 访问您的网站

```
网站地址：http://您的用户名.pythonanywhere.com
```

### 登录测试

```
管理员账户：admin / admin123
登记员账户：registrar / reg123
```

---

## ⚙️ 配置优化

### 自定义域名（可选）

免费版域名格式：`您的用户名.pythonanywhere.com`

### 环境变量设置

在Web应用配置中的 "Environment variables" 部分添加：
```
FLASK_ENV = production
SECRET_KEY = your-secret-key
```

### 日志查看

- 点击 "Log files" 查看访问日志和错误日志
- 监控应用运行状态

---

## 🔧 常见问题解决

### Q: 网站显示500错误？
```
A: 1. 检查错误日志：Web页面 → Log files → Error log
   2. 确认WSGI文件配置正确
   3. 检查数据库连接配置
```

### Q: 数据库连接失败？
```
A: 1. 确认数据库已创建
   2. 检查config.py中的数据库配置
   3. 确认安装了PyMySQL
```

### Q: 模块导入错误？
```
A: 1. 确认已安装requirements.txt中的依赖
   2. 使用 pip3.10 install --user 安装
   3. 检查Python版本设置
```

### Q: CPU时间超限？
```
A: 1. 检查Tasks页面的使用情况
   2. 优化代码减少CPU使用
   3. 考虑升级付费计划（$5/月）
```

---

## 📊 资源监控

### 查看使用情况

在Dashboard页面可以看到：
- ✅ **CPU使用时间**：每日重置
- ✅ **存储空间使用**：500MB限制
- ✅ **数据库大小**：500MB限制
- ✅ **网站访问统计**

### 使用建议

- 定期检查CPU使用情况
- 合理使用数据库存储
- 及时清理不需要的文件

---

## 🎯 成本对比

| 平台 | 月费用 | 年费用 | 信用卡 | 限制 |
|------|--------|--------|--------|------|
| **Railway** | $5 | $60 | 需要 | 最低消费 |
| **Render** | $0 | $0 | 需要 | 休眠机制 |
| **PythonAnywhere** | $0 | $0 | 不需要 | CPU时间 |

**🏆 PythonAnywhere胜出：真正免费 + 无需信用卡！**

---

## 🚀 升级选项（可选）

如果需要更多资源：

### Hacker计划 ($5/月)
- ✅ 无CPU时间限制
- ✅ 2个Web应用
- ✅ 更多存储空间
- ✅ SSH访问

### Web Developer计划 ($12/月)
- ✅ 无限Web应用
- ✅ 自定义域名
- ✅ SSL证书

---

## 🎊 部署完成后

### 分享给用户

```
🏢 自习室管理系统已上线！
🌐 网址：http://您的用户名.pythonanywhere.com
👤 联系管理员获取登录账户
📱 支持手机、平板、电脑访问
🆓 永久免费，24/7在线服务
```

### 管理建议

1. **定期备份数据**：导出重要数据
2. **监控使用情况**：检查CPU和存储使用
3. **更新维护**：定期更新代码和依赖

---

## 📞 需要帮助？

我将全程协助您完成部署：

1. **🔧 技术支持**：解决部署问题
2. **📋 配置协助**：帮助修改配置文件
3. **🐛 问题排查**：解决运行错误
4. **📊 优化建议**：提高应用性能

**现在开始部署PythonAnywhere，彻底告别月费！** 🎉

---

**准备好了吗？让我们开始第一步：注册PythonAnywhere账户！** 🚀 