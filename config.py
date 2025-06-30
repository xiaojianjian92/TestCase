import os
import secrets
from datetime import timedelta
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据库目录
SQLALCHEMY_DATABASE_DIR = os.path.join(BASE_DIR, 'database')
if not os.path.exists(SQLALCHEMY_DATABASE_DIR):
    os.makedirs(SQLALCHEMY_DATABASE_DIR)


class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_TOKEN_EXPIRES = timedelta(days=30)

    # 配置flask-security
    SECURITY_PASSWORD_SALT = secrets.SystemRandom().getrandbits(128)    
    SECURITY_REGISTERABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_CONFIRMABLE = False
    SECURITY_CHANGEABLE = False
    SECURITY_LOGINABLE = False
    SECURITY_REGISTER_URL = '/auth/register'
    SECURITY_LOGIN_URL = '/auth/login'
    SECURITY_LOGOUT_URL = '/auth/logout'
    SECURITY_POST_LOGOUT_VIEW = '/auth/login'

    # 配置flask-admin
    FLASK_ADMIN_SWATCH = 'superhero'
    FLASK_ADMIN_URL = '/admin'
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = '12345678'    


    # 配置flask-cache
    CACHE_TYPE = 'filesystem'
    CACHE_DEFAULT_TIMEOUT = 3600
    CACHE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache')
    CACHE_THRESHOLD = 500

    # 配置文件上传
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'xlsx', 'xlsx', 'csv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # 配置日志
    LOG_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs')
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.path.join(LOG_FOLDER, 'app.log')


# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{SQLALCHEMY_DATABASE_DIR}/test_case_dev.db'

# 生产环境配置
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI =f'sqlite:///{SQLALCHEMY_DATABASE_DIR}/test_case.db'
    # secure cookies and session data
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
