from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from config import config

# 全局变量
db = SQLAlchemy()
login_manager = LoginManager()

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' 或 'registrar'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 座位模型
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(10), unique=True, nullable=False)  # A01-A30, B01-B09
    is_occupied = db.Column(db.Boolean, default=False)
    occupant_name = db.Column(db.String(100))
    card_type = db.Column(db.String(50))  # 办卡类型
    expiry_date = db.Column(db.Date)  # 到期时间
    notes = db.Column(db.Text)  # 备注
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_by = db.Column(db.Integer, db.ForeignKey('user.id'))

# 操作记录模型
class OperationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    operation = db.Column(db.String(50), nullable=False)  # 操作类型
    old_data = db.Column(db.Text)  # 修改前的数据
    new_data = db.Column(db.Text)  # 修改后的数据
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV') or 'default'
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # 配置Flask-Login
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 注册路由
    register_routes(app)
    
    return app

def register_routes(app):
    """注册所有路由"""
    
    def format_seat_data_for_log(data):
        """格式化座位数据为用户友好的显示格式"""
        if not data:
            return "无数据"
        
        # 如果数据是字符串，尝试解析为字典
        if isinstance(data, str):
            try:
                # 尝试解析字符串格式的字典
                import ast
                data = ast.literal_eval(data)
            except:
                # 如果解析失败，返回原始字符串
                return data
        
        formatted_items = []
        
        # 格式化占用状态
        if 'is_occupied' in data:
            status = "已占用" if data['is_occupied'] else "空闲"
            formatted_items.append(f"状态: {status}")
        
        # 格式化使用者姓名
        if 'occupant_name' in data:
            name = data['occupant_name'] or "无"
            formatted_items.append(f"使用者: {name}")
        
        # 格式化办卡类型
        if 'card_type' in data:
            card_type = data['card_type'] or "无"
            formatted_items.append(f"卡类型: {card_type}")
        
        # 格式化到期时间
        if 'expiry_date' in data:
            expiry = data['expiry_date'] or "无期限"
            if expiry != "无期限":
                try:
                    # 如果是日期字符串，格式化显示
                    formatted_date = datetime.strptime(expiry, '%Y-%m-%d').strftime('%Y年%m月%d日')
                    formatted_items.append(f"到期时间: {formatted_date}")
                except:
                    formatted_items.append(f"到期时间: {expiry}")
            else:
                formatted_items.append(f"到期时间: {expiry}")
        
        # 格式化备注
        if 'notes' in data:
            notes = data['notes'] or "无"
            if len(notes) > 20:
                notes = notes[:20] + "..."
            formatted_items.append(f"备注: {notes}")
        
        return " | ".join(formatted_items)

    # 健康检查路由
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'xunshanapp'}, 200
    
    # 主页 - 添加登录要求
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    # 登录页面
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                return jsonify({'success': True, 'role': user.role, 'username': user.username})
            else:
                return jsonify({'success': False, 'message': '用户名或密码错误'})
        
        return render_template('login.html')

    # 登出
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    # 数据库管理页面（仅管理员）
    @app.route('/database')
    @login_required
    def database_view():
        if current_user.role != 'admin':
            return redirect(url_for('index'))
        return render_template('database.html')

    # 获取数据库统计信息
    @app.route('/api/database/stats')
    @login_required
    def get_database_stats():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        # 基本统计
        total_seats = Seat.query.count()
        occupied_seats = Seat.query.filter_by(is_occupied=True).count()
        available_seats = total_seats - occupied_seats
        
        # 即将过期统计
        from sqlalchemy import text, and_
        expiring_soon = db.session.execute(text("""
            SELECT COUNT(*) FROM seat 
            WHERE is_occupied = 1 
            AND expiry_date IS NOT NULL 
            AND DATE(expiry_date) BETWEEN DATE('now') AND DATE('now', '+7 days')
        """)).scalar()
        
        # 已过期统计
        expired = db.session.execute(text("""
            SELECT COUNT(*) FROM seat 
            WHERE is_occupied = 1 
            AND expiry_date IS NOT NULL 
            AND DATE(expiry_date) < DATE('now')
        """)).scalar()
        
        # 卡类型统计
        card_stats = db.session.execute(text("""
            SELECT card_type, COUNT(*) as count
            FROM seat 
            WHERE is_occupied = 1 AND card_type IS NOT NULL 
            GROUP BY card_type
        """)).fetchall()
        
        # 用户统计
        total_users = User.query.count()
        admin_count = User.query.filter_by(role='admin').count()
        registrar_count = User.query.filter_by(role='registrar').count()
        
        # 操作记录统计
        total_operations = OperationLog.query.count()
        
        return jsonify({
            'seat_stats': {
                'total': total_seats,
                'occupied': occupied_seats,
                'available': available_seats,
                'expiring_soon': expiring_soon,
                'expired': expired
            },
            'card_stats': [{'type': row[0], 'count': row[1]} for row in card_stats],
            'user_stats': {
                'total': total_users,
                'admin': admin_count,
                'registrar': registrar_count
            },
            'operation_stats': {
                'total': total_operations
            }
        })

    # 获取所有用户数据
    @app.route('/api/database/users')
    @login_required
    def get_all_users():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'role': user.role,
                'role_name': '管理员' if user.role == 'admin' else '登记员',
                'created_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify(users_data)

    # 获取单个用户数据
    @app.route('/api/database/users/<int:user_id>')
    @login_required
    def get_user(user_id):
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'role_name': '管理员' if user.role == 'admin' else '登记员',
            'created_at': user.created_at.isoformat() if user.created_at else None
        })

    # 新增用户
    @app.route('/api/database/users', methods=['POST'])
    @login_required
    def create_user():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '').strip()
        
        # 验证数据
        if not username or not password or not role:
            return jsonify({'success': False, 'message': '请填写完整信息'}), 400
        
        if role not in ['admin', 'registrar']:
            return jsonify({'success': False, 'message': '角色无效'}), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        
        # 创建新用户
        try:
            new_user = User(username=username, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True, 'message': '用户创建成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'创建用户失败: {str(e)}'}), 500

    # 更新用户
    @app.route('/api/database/users/<int:user_id>', methods=['PUT'])
    @login_required
    def update_user(user_id):
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        role = data.get('role', '').strip()
        
        # 验证数据
        if not username or not role:
            return jsonify({'success': False, 'message': '请填写完整信息'}), 400
        
        if role not in ['admin', 'registrar']:
            return jsonify({'success': False, 'message': '角色无效'}), 400
        
        # 检查用户名是否与其他用户冲突
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'success': False, 'message': '用户名已存在'}), 400
        
        try:
            user.username = username
            user.role = role
            if password:  # 如果提供了新密码
                user.set_password(password)
            
            db.session.commit()
            return jsonify({'success': True, 'message': '用户更新成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'更新用户失败: {str(e)}'}), 500

    # 删除用户
    @app.route('/api/database/users/<int:user_id>', methods=['DELETE'])
    @login_required
    def delete_user(user_id):
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        user = User.query.get_or_404(user_id)
        
        # 防止删除当前登录用户
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': '不能删除当前登录用户'}), 400
        
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': '用户删除成功'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': f'删除用户失败: {str(e)}'}), 500

    # 获取所有座位详细数据
    @app.route('/api/database/seats_detail')
    @login_required
    def get_seats_detail():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        seats = db.session.query(Seat, User).outerjoin(User, Seat.updated_by == User.id).all()
        seats_data = []
        
        for seat, updated_user in seats:
            seats_data.append({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_occupied': seat.is_occupied,
                'status': '已占用' if seat.is_occupied else '空闲',
                'occupant_name': seat.occupant_name,
                'card_type': seat.card_type,
                'expiry_date': seat.expiry_date.isoformat() if seat.expiry_date else None,
                'notes': seat.notes,
                'updated_at': seat.updated_at.isoformat() if seat.updated_at else None,
                'updated_by': updated_user.username if updated_user else None
            })
        
        return jsonify(seats_data)

    # 获取详细操作记录
    @app.route('/api/database/logs_detail')
    @login_required
    def get_logs_detail():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        # 获取最近100条记录
        logs = db.session.query(OperationLog, User, Seat)\
            .join(User, OperationLog.user_id == User.id)\
            .join(Seat, OperationLog.seat_id == Seat.id)\
            .order_by(OperationLog.timestamp.desc())\
            .limit(100).all()
        
        logs_data = []
        for log, user, seat in logs:
            logs_data.append({
                'id': log.id,
                'username': user.username,
                'seat_number': seat.seat_number,
                'operation': log.operation,
                'timestamp': log.timestamp.isoformat(),
                'old_data': format_seat_data_for_log(log.old_data),
                'new_data': format_seat_data_for_log(log.new_data)
            })
        
        return jsonify(logs_data)

    # 导出数据库数据
    @app.route('/api/database/export')
    @login_required
    def export_database():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        try:
            import json
            from flask import make_response
            
            # 收集所有数据
            users = User.query.all()
            seats = Seat.query.all()
            logs = db.session.query(OperationLog, User, Seat)\
                .join(User, OperationLog.user_id == User.id)\
                .join(Seat, OperationLog.seat_id == Seat.id)\
                .order_by(OperationLog.timestamp.desc()).all()
            
            export_data = {
                'export_time': datetime.now().isoformat(),
                'users': [{
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                } for user in users],
                'seats': [{
                    'id': seat.id,
                    'seat_number': seat.seat_number,
                    'is_occupied': seat.is_occupied,
                    'occupant_name': seat.occupant_name,
                    'card_type': seat.card_type,
                    'expiry_date': seat.expiry_date.isoformat() if seat.expiry_date else None,
                    'notes': seat.notes,
                    'updated_at': seat.updated_at.isoformat() if seat.updated_at else None
                } for seat in seats],
                'operation_logs': [{
                    'id': log.id,
                    'username': user.username,
                    'seat_number': seat.seat_number,
                    'operation': log.operation,
                    'timestamp': log.timestamp.isoformat(),
                    'old_data': log.old_data,
                    'new_data': log.new_data
                } for log, user, seat in logs]
            }
            
            # 创建响应
            response = make_response(json.dumps(export_data, ensure_ascii=False, indent=2))
            response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response.headers['Content-Disposition'] = f'attachment; filename=database_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            return response
            
        except Exception as e:
            return jsonify({'error': f'导出失败: {str(e)}'}), 500

    # 获取所有座位信息
    @app.route('/api/seats')
    @login_required
    def get_seats():
        seats = Seat.query.all()
        seats_data = []
        for seat in seats:
            seats_data.append({
                'id': seat.id,
                'seat_number': seat.seat_number,
                'is_occupied': seat.is_occupied,
                'occupant_name': seat.occupant_name,
                'card_type': seat.card_type,
                'expiry_date': seat.expiry_date.isoformat() if seat.expiry_date else None,
                'notes': seat.notes,
                'updated_at': seat.updated_at.isoformat() if seat.updated_at else None
            })
        return jsonify(seats_data)

    # 更新座位信息
    @app.route('/api/seats/<int:seat_id>', methods=['PUT'])
    @login_required
    def update_seat(seat_id):
        seat = Seat.query.get_or_404(seat_id)
        data = request.get_json()
        
        # 记录操作前的数据
        old_data = {
            'is_occupied': seat.is_occupied,
            'occupant_name': seat.occupant_name,
            'card_type': seat.card_type,
            'expiry_date': seat.expiry_date.isoformat() if seat.expiry_date else None,
            'notes': seat.notes
        }
        
        # 准备新数据，确保数据类型一致性
        new_data = {
            'is_occupied': data.get('is_occupied', seat.is_occupied),
            'occupant_name': data.get('occupant_name', '').strip() or None,
            'card_type': data.get('card_type', '').strip() or None,
            'expiry_date': data.get('expiry_date') if data.get('expiry_date') else None,
            'notes': data.get('notes', '').strip() or None
        }
        
        # 标准化旧数据格式
        old_data_normalized = {
            'is_occupied': old_data['is_occupied'],
            'occupant_name': old_data['occupant_name'],
            'card_type': old_data['card_type'],
            'expiry_date': old_data['expiry_date'],
            'notes': old_data['notes']
        }
        
        # 检查数据是否发生变化
        data_changed = False
        for key in old_data_normalized:
            if old_data_normalized[key] != new_data[key]:
                data_changed = True
                break
        
        # 只有数据真的发生变化时才更新和记录
        if data_changed:
            # 更新座位信息
            seat.is_occupied = new_data['is_occupied']
            seat.occupant_name = new_data['occupant_name']
            seat.card_type = new_data['card_type']
            
            if new_data['expiry_date']:
                seat.expiry_date = datetime.strptime(new_data['expiry_date'], '%Y-%m-%d').date()
            else:
                seat.expiry_date = None
            
            seat.notes = new_data['notes']
            seat.updated_at = datetime.utcnow()
            seat.updated_by = current_user.id
            
            # 记录操作日志
            log = OperationLog(
                user_id=current_user.id,
                seat_id=seat.id,
                operation='update_seat',
                old_data=format_seat_data_for_log(old_data),
                new_data=format_seat_data_for_log(new_data)
            )
            
            db.session.add(log)
            db.session.commit()
            
            return jsonify({'success': True, 'message': '座位信息更新成功'})
        else:
            # 没有变化，不需要更新
            return jsonify({'success': True, 'message': '座位信息无变化'})

    # 获取操作记录（仅管理员）
    @app.route('/api/logs')
    @login_required
    def get_operation_logs():
        if current_user.role != 'admin':
            return jsonify({'error': '权限不足'}), 403
        
        try:
            logs = db.session.query(OperationLog, User, Seat)\
                .join(User, OperationLog.user_id == User.id)\
                .join(Seat, OperationLog.seat_id == Seat.id)\
                .order_by(OperationLog.timestamp.desc())\
                .all()
            logs_data = []
            
            for log, user, seat in logs:
                logs_data.append({
                    'id': log.id,
                    'username': user.username,
                    'seat_number': seat.seat_number,
                    'operation': log.operation,
                    'old_data': format_seat_data_for_log(log.old_data),
                    'new_data': format_seat_data_for_log(log.new_data),
                    'timestamp': log.timestamp.isoformat()
                })
            
            return jsonify(logs_data)
        except Exception as e:
            print(f"操作记录查询错误: {e}")
            return jsonify({'error': '查询失败'}), 500

def init_db():
    """初始化数据库"""
    # 创建默认管理员
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
    
    # 创建默认登记员
    if not User.query.filter_by(username='registrar').first():
        registrar = User(username='registrar', role='registrar')
        registrar.set_password('reg123')
        db.session.add(registrar)
    
    # 创建座位
    if not Seat.query.first():
        # A区座位 A01-A30
        for i in range(1, 31):
            seat_number = f"A{i:02d}"
            seat = Seat(seat_number=seat_number)
            db.session.add(seat)
        
        # B区座位 B01-B09
        for i in range(1, 10):
            seat_number = f"B{i:02d}"
            seat = Seat(seat_number=seat_number)
            db.session.add(seat)
    
    db.session.commit()
    print("数据库初始化完成！")
    print("默认管理员: admin / admin123")
    print("默认登记员: registrar / reg123")

if __name__ == '__main__':
    # 开发环境直接运行
    app = create_app('development')
    with app.app_context():
        db.create_all()
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 