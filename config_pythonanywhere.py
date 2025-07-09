import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 根据环境选择数据库
    if os.environ.get('FLASK_ENV') == 'production' and 'pythonanywhere' in os.environ.get('SERVER_NAME', ''):
        # PythonAnywhere MySQL配置
        MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
        MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
        MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
        MYSQL_DB = os.environ.get('MYSQL_DB') or 'xunshanapp'
        
        SQLALCHEMY_DATABASE_URI = (
            f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
        )
    else:
        # 本地开发使用SQLite
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'study_room.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 