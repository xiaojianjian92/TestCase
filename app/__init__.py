from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
from flask_security import Security, SQLAlchemyUserDatastore
import os

# 初始化数据库
db = SQLAlchemy()
# 初始化登录管理器
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 设置登录视图
# 初始化迁移扩展
migrate = Migrate()
# 初始化安全扩展
security = Security()




def create_app(config_class=config):
    
    app = Flask(__name__)  
    env = os.getenv('FLASK_ENV', 'development')  # 获取环境变量，默认为开发环境
    app.config.from_object(config_class[env])  # 根据环境加载配置

    # 初始化扩展应用
    db.init_app(app)
    login_manager.init_app(app)
 

    from .routes.admin import init_admin  # 导入初始化Admin的函数
    init_admin(app)  # 初始化Admin

    migrate.init_app(app, db)

    from .models import User, Role  
    security.init_app(app, SQLAlchemyUserDatastore(db, User, Role), register_blueprint=False)    

    from .routes.auth import auth_bp  
    app.register_blueprint(auth_bp)

    from .routes.main import main_bp  
    app.register_blueprint(main_bp)  

    from .routes.project import project_bp  
    app.register_blueprint(project_bp) 

    from .routes.testcase import testcase_bp  
    app.register_blueprint(testcase_bp) 

    # 404错误处理
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    # 500错误处理
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500

    # 其他错误处理
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     return jsonify({"error": "发生未知错误，请联系管理员"})


    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User  # 延迟导入，避免循环依赖
    return User.query.get(int(user_id))