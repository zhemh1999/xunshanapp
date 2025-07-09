import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xunshanapp_secret_key_2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///study_room.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # 8小时后自动退出
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    # 生产环境建议设置更强的密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key-here'
    # 启用HTTPS相关安全设置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 