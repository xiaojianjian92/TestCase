from app import create_app
from app.models import db
from app.utils.helper import generate_fs_uniquifier

app = create_app()

if __name__ == '__main__':

    # 初始化管理员角色和用户
    with app.app_context():
        from app.models import Role, User # 延迟导入，避免循环依赖
        db.create_all()  # 创建数据库表
        # 创建默认角色
        roles = {'admin': '管理员', 'user': '普通用户'}
        for role_name, role_description in roles.items():
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=role_description)
                db.session.add(role)
                db.session.commit()
            
        # 创建初始管理员用户（邮箱：admin@example.com）
        if not User.query.filter_by(email='admin@example.com').first():  # 检查是否已经存在管理员用户
            admin_user = User(
                username='admin',  
                active=True, 
                email='admin@example.com', 
                fs_uniquifier=generate_fs_uniquifier()  # 生成唯一标识符
            )
            admin_user.set_password('12345678') 
            admin_role = Role.query.filter_by(name='admin').first()
            if admin_role: 
                admin_user.role = admin_role 
            db.session.add(admin_user)           
            db.session.commit() 

    app.run(host='0.0.0.0', port=5000)
