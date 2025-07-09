# 自习室管理系统

一个专为自习室设计的座位管理系统，支持Web和Android平台。

## 功能特点

- 🪑 **座位管理**: 管理39个座位（A01-A30, B01-B09）
- 👥 **用户权限**: 支持管理员和登记员两种角色
- 📊 **实时统计**: 显示座位占用情况和到期提醒
- 📱 **多平台**: 支持Web浏览器和Android设备
- 📝 **操作记录**: 管理员可查看所有操作历史
- 🔍 **智能筛选**: 按座位状态、卡片到期情况筛选

## 系统架构

- **后端**: Python Flask + SQLite
- **前端**: Bootstrap + jQuery + HTML5
- **数据库**: SQLite（可扩展到MySQL/PostgreSQL）
- **移动端**: Web App（响应式设计）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

### 3. 访问系统

打开浏览器访问：http://localhost:5000

### 4. 默认账户

- **管理员**: admin / admin123
- **登记员**: registrar / reg123

## 座位信息管理

### 座位编号
- A区：A01 - A30（30个座位）
- B区：B01 - B09（9个座位）
- 总计：39个座位

### 办卡类型
- 月卡
- 季卡
- 半年卡
- 年卡
- 临时卡

### 状态显示
- 🟢 **绿色**: 空闲座位
- 🔴 **红色**: 已占用座位
- 🟡 **黄色**: 即将过期（7天内）

## 用户权限

### 登记员权限
- 查看所有座位状态
- 修改座位信息
- 更新人员信息和办卡类型

### 管理员权限
- 登记员的所有权限
- 查看操作记录
- 监控系统使用情况

## API接口

### 认证接口
- `POST /login` - 用户登录
- `GET /logout` - 用户登出

### 座位管理
- `GET /api/seats` - 获取所有座位信息
- `PUT /api/seats/<id>` - 更新座位信息

### 操作记录
- `GET /api/logs` - 获取操作记录（仅管理员）

## Android应用

系统采用响应式设计，可直接在Android浏览器中使用，或者可以基于WebView开发原生Android应用。

### Android开发建议
1. 使用WebView加载Web界面
2. 添加离线缓存功能
3. 集成条码扫描功能
4. 添加推送通知

## 数据库结构

### 用户表 (User)
- id: 主键
- username: 用户名
- password_hash: 密码哈希
- role: 角色（admin/registrar）
- created_at: 创建时间

### 座位表 (Seat)
- id: 主键
- seat_number: 座位编号
- is_occupied: 是否占用
- occupant_name: 使用者姓名
- card_type: 办卡类型
- expiry_date: 到期时间
- notes: 备注
- updated_at: 更新时间
- updated_by: 更新人

### 操作记录表 (OperationLog)
- id: 主键
- user_id: 操作用户ID
- seat_id: 座位ID
- operation: 操作类型
- old_data: 修改前数据
- new_data: 修改后数据
- timestamp: 操作时间

## 部署说明

### 开发环境
```bash
python app.py
```

### 生产环境
建议使用Gunicorn + Nginx部署：

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 扩展功能

- [ ] 座位预约功能
- [ ] 微信/支付宝支付集成
- [ ] 数据导出功能
- [ ] 会员积分系统
- [ ] 多自习室支持
- [ ] 实时通知推送

## 技术支持

如有问题或建议，请联系开发团队。

## 版本历史

- v1.0.0 - 基础功能实现
  - 座位管理
  - 用户权限控制
  - 操作记录
  - 响应式Web界面

## 许可证

MIT License 