from datetime import datetime
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.utils.helper import generate_fs_uniquifier


# 角色模型
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)      
    description = db.Column(db.String(255))
    users = db.relationship('User', back_populates='role', lazy=True)    

    def __str__(self):
        return self.name


# 用户模型
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, info={'label': '激活'})      
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=generate_fs_uniquifier())  # Flask-Security 4.0.0 版本开始，fs_uniquifier 字段成为必需项，用于存储用户的唯一标识符
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)   
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 用户与项目的关系
    projects = db.relationship('Project', back_populates='creator', lazy=True)
    # 用户与测试用例的关系
    test_cases = db.relationship('TestCase', back_populates='creator', lazy=True)
    # 显式定义关系
    role = db.relationship('Role', back_populates='users')

    # 密码哈希处理
    def set_password(self, password):
        # 设置密码哈希
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # 检查密码是否匹配
        return check_password_hash(self.password, password)

  
# 项目模型
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)  
    
    # 项目与用户的关系
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))    
    # 显示定义关系
    creator = db.relationship('User', back_populates='projects')
    # 项目与测试用例的关系
    test_cases = db.relationship('TestCase', back_populates='project', lazy=True)      


    def __str__(self):
        return self.name


# 测试用例模型
class TestCase(db.Model):
    __tablename__ = 'test_case'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) # 主键ID  
    title = db.Column(db.String(100), nullable=False)   # 用例标题
    module = db.Column(db.String(50))    # 用例所属模块
    case_type = db.Column(db.String(50))    # 用例类型（功能/性能/兼容性）
    case_level = db.Column(db.String(20))  # 用例等级（如P0-P3）
    preconditions = db.Column(db.Text)  # 前置条件
    test_steps = db.Column(db.Text)  # 测试步骤
    expected_result = db.Column(db.Text)   # 预期结果
    test_result = db.Column(db.String(20))  # 测试结果（通过/失败/未执行）
    remarks = db.Column(db.Text)  # 备注
    create_time = db.Column(db.DateTime, default=datetime.now) # 创建时间

    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # 更新时间    
    # 关联项目
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False) # 所属项目ID
    # 关联创建者
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)    # 创建者ID
    # 显示定义关系
    creator = db.relationship('User', back_populates='test_cases')
    # 显示定义项目关系
    project = db.relationship('Project', back_populates='test_cases')

    def __str__(self):
        return f"{self.project_id}- {self.title}"








