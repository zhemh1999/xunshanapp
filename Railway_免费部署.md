# 🚀 Railway 免费部署（推荐）

## 🎯 为什么选择Railway？

- ✅ **完全免费** - 不需要付费
- ✅ **24/7在线** - 不需要您的电脑保持开启
- ✅ **自动部署** - 代码更新自动部署
- ✅ **免费域名** - 提供https://xxx.railway.app域名
- ✅ **简单易用** - 几分钟即可完成部署

## 📋 准备工作

1. **GitHub账户** - 如果没有，请先注册：https://github.com/
2. **代码上传** - 将您的代码上传到GitHub仓库

## 🔧 步骤1：上传代码到GitHub

### 方法1：使用Git命令行
```bash
# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "初始化自习室管理系统"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/您的用户名/xunshanapp.git

# 推送代码
git push -u origin main
```

### 方法2：使用GitHub Desktop
1. 下载GitHub Desktop：https://desktop.github.com/
2. 创建新仓库
3. 将项目文件拖入
4. 提交并推送

### 方法3：网页上传
1. 访问 https://github.com/
2. 点击 "New repository"
3. 创建仓库后，点击 "uploading an existing file"
4. 将所有文件拖入上传

## 🚀 步骤2：部署到Railway

1. **访问Railway**：https://railway.app/

2. **使用GitHub登录**：
   - 点击 "Login with GitHub"
   - 授权Railway访问您的GitHub

3. **创建新项目**：
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您的 `xunshanapp` 仓库

4. **等待部署**：
   - Railway会自动检测Python项目
   - 自动安装依赖并部署
   - 通常需要2-5分钟

5. **获取访问地址**：
   - 部署完成后，点击项目
   - 在 "Deployments" 页面找到您的域名
   - 形如：`https://xunshanapp-production.up.railway.app`

## 🎉 步骤3：测试访问

1. **点击您的Railway域名**
2. **应该看到登录页面**
3. **使用默认账户登录**：
   - 管理员：admin / admin123
   - 登记员：registrar / reg123

## 🔧 配置环境变量（可选）

如果需要自定义配置：

1. **进入项目设置**：
   - 点击项目名称
   - 选择 "Variables" 标签

2. **添加环境变量**：
   ```
   FLASK_ENV=production
   SECRET_KEY=您的密钥
   ```

## 📱 自定义域名（可选）

1. **在Railway项目中**：
   - 点击 "Settings"
   - 选择 "Domains"
   - 点击 "Custom Domain"
   - 输入您的域名（如：xunshanapp.yourdomain.com）

2. **配置DNS**：
   - 在您的域名提供商处
   - 添加CNAME记录指向Railway提供的地址

## 🔄 自动更新部署

每次您更新GitHub代码，Railway会自动重新部署：

1. **修改代码**
2. **推送到GitHub**：
   ```bash
   git add .
   git commit -m "更新功能"
   git push
   ```
3. **Railway自动部署** - 无需手动操作

## 📊 监控和日志

1. **查看部署日志**：
   - 在Railway项目中点击 "Deployments"
   - 选择最新部署查看日志

2. **监控运行状态**：
   - 在 "Metrics" 标签查看CPU、内存使用情况

## 🆘 常见问题

**Q: 部署失败怎么办？**
A: 检查日志，通常是依赖安装问题。确保requirements.txt正确。

**Q: 如何查看应用日志？**
A: 在Railway项目中点击 "Deployments" → 选择部署 → 查看日志

**Q: 数据会丢失吗？**
A: Railway每次部署都是全新环境，建议定期备份数据

**Q: 如何停止应用？**
A: 在Railway项目设置中可以暂停或删除项目

**Q: 免费版有限制吗？**
A: 有一定的使用限制，但对于小型应用完全够用

## 💡 优化建议

1. **数据持久化**：
   - 考虑使用Railway的PostgreSQL插件
   - 或定期备份SQLite数据

2. **性能优化**：
   - 减少不必要的依赖
   - 优化数据库查询

3. **安全设置**：
   - 及时修改默认密码
   - 设置强密钥

## 🎊 成功部署！

如果一切顺利，您现在有了：

- ✅ 24/7在线的自习室管理系统
- ✅ 专业的https域名
- ✅ 自动化部署流程
- ✅ 免费的云服务

**您的系统访问地址：**
`https://您的项目名.up.railway.app`

**分享给用户：**
- 发送链接给员工
- 贴在公告板上
- 制作二维码供扫描

---

## 📞 需要帮助？

如果遇到任何问题：
1. 查看Railway部署日志
2. 检查GitHub代码是否正确
3. 参考本指南重新操作
4. 联系技术支持

**恭喜！您的自习室管理系统已经成功部署到云端！** 🎉 