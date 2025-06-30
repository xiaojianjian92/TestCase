from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin
from flask_admin.menu import MenuLink
from flask import redirect, url_for, flash
from app.models import User, Role, Project, TestCase
from flask_login import current_user
from app import db
from wtforms import PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from werkzeug.security import generate_password_hash


# 自定义AdminIndexView，用于管理后台首页
class InnoAdminIndexView(AdminIndexView):
    def is_accessible(self):  
        return current_user.is_authenticated and current_user.role.name == 'admin'
    
    def inaccessible_callback(self, name, **kwargs): 
        flash('您没有访问权限', 'error')
        return redirect(url_for('auth.login'))  

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:  
            return redirect(url_for('auth.login'))  
        # 首页显示数据
        user_count = User.query.count()  # 用户数量
        role_count = Role.query.count()  # 角色数量
        project_count = Project.query.count()  # 项目数量
        test_case_count = TestCase.query.count()  # 测试用例数量
        return self.render('admin/index.html', user_count=user_count,role_count=role_count, project_count=project_count, test_case_count=test_case_count)  
    

class UserModelView(ModelView):    
    # 列显示属性
    column_list = ('id', 'username', 'email', 'active', 'created_at', 'role', 'fs_uniquifier')  
    column_labels = { 
        'id': '用户ID',        
        'username': '用户名',
        'email': '邮箱',  
        'role': '角色',
        'active': '激活状态',
        'fs_uniquifier': '唯一标识符',
        'created_at': '创建时间'
    }
    column_default_sort = ('created_at', True)  # 默认按创建时间降序排序      

    # 视图行为属性
    page_size = 20
    column_display_actions = True
    create_modal = True
    edit_modal = True
    details_modal = True    
    
    # 表单配置属性
    form_columns = ('username', 'email', 'password', 'confirm_password', 'active', 'role')  # 指定表单中显示的字段
    # 新增确认密码字段
    form_extra_fields = {        
        'confirm_password': PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='密码不匹配')], render_kw={'placeholder': '请再次输入密码'})
    }
    form_overrides = {
        'password': PasswordField        
    }
    # 修改已有字段
    form_args = {
        'username': {
            'label': '用户名',
            'validators': [DataRequired(), Length(min=3, max=20)],
            'render_kw': {'placeholder': '请输入3-20位的用户名'}
        },
        'password': {
            'label': '密码',            
            'validators': [DataRequired(),
            Length(min=8, message="密码至少8位"),  # 密码长度限制
            Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}", message="密码必须包含大写字母、小写字母、数字和特殊字符")],  # 密码复杂度限制
            'render_kw': {'placeholder': '密码至少8位且必须包含大写字母、小写字母、数字和特殊字符'}
        },
        'email': {
            'label': '邮箱',            
            'validators': [DataRequired(), Email(message='请输入有效的邮箱地址')],
            'render_kw': {'placeholder': '请输入有效的邮箱地址'}
        }
    }    

    def handle_view_exception(self, exc):
        flash(f"操作失败：{str(exc)}", 'error')
        return redirect(url_for('admin.index'))
        
    
    def on_model_change(self, form, model, is_created):
        if not is_created:
            if not form.password.data:
                original_password = self.session.query(self.model).get(model.id).password
                model.password = original_password
                return
        if form.password.data:
            model.password = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)


    def on_model_delete(self, model):
        if model == current_user:
            raise Exception('不能删除当前用户')
            
        if model.role.name == 'admin':
            raise Exception('不能删除管理员角色的用户')        
        super().on_model_delete(model)

    

class RoleModelView(ModelView): 
    #列显示属性
    column_list = ('id', 'name', 'description', )  
    column_labels = {  
        'id': 'ID',
        'name': '角色名称',
        'description': '描述' 
    }

    # 视图行为属性
    page_size = 20
    column_display_actions = True
    create_modal = True
    edit_modal = True
    details_modal = True  

    # 表单配置属性
    form_columns = ('name', 'description' )  
    form_args = {
        'name': {
            'label': '角色名称',
            'validators': [DataRequired(), Length(min=3, max=20)],
            'render_kw': {'placeholder': '请输入3-20位的角色名称'}
        },
        'description': {
            'label': '描述',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入描述'}
        }
    }


    def handle_view_exception(self, exc):
        flash(f"操作失败：{str(exc)}", 'error')
        return redirect(url_for('admin.index'))

    def on_model_delete(self, model):
        
        # 阻止删除默认角色
        if model.name in ["admin", "user"]:
            raise Exception('不能删除默认角色')            
        
        # 阻止删除关联用户
        if model.users:
            raise Exception('该角色有关联用户，不能删除')        

        # 其他情况下允许删除
        return super().on_model_delete(model)


class ProjectModelView(ModelView):
    # 列显示属性
    column_list = ('id', 'name', 'description', 'creator', 'created_at')  
    column_labels = {  
        'id': '项目ID',
        'name': '项目名称',
        'description': '项目描述',
        'creator': '创建者',
        'created_at': '创建时间'
    }
    column_default_sort = ('created_at', True)  # 默认按创建时间降序排序

    def format_creator(self, context, model, name):
        return model.creator.username if model.creator else '未知创建者'
    
    column_formatters = {
        'creator': format_creator
    }

    # 表单配置属性
    form_columns = ('name', 'description')  
    form_args = {
        'name': {
            'label': '项目名称',
            'validators': [DataRequired(), Length(min=3, max=20)],
            'render_kw': {'placeholder': '请输入3-20位的项目名称'}
        },
        'description': {
            'label': '描述',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入描述'}
        }
    }

    # 视图行为属性
    page_size = 20
    column_display_actions = True
    create_modal = True
    edit_modal = True
    details_modal = True      

    def handle_view_exception(self, exc):
        flash(f"操作失败：{str(exc)}", 'error')
        return redirect(url_for('admin.index'))
    


class TestCaseModelView(ModelView):
    # 列显示属性
    column_list = ('id', 'title', 'module', 'case_type', 'case_level', 'preconditions', 'test_steps', 'expected_result', 'test_result', 'remarks', 'create_time', 'update_time','project', 'creator')  # 显示的列
    column_auto_width = False
    column_auto_select_related = True
    column_labels = {
        'id': '用例ID',
        'title': '用例标题',
        'module': '所属模块',
        'case_type': '用例类型',
        'case_level': '用例等级',
        'preconditions': '前置条件',
        'test_steps': '测试步骤',
        'expected_result': '预期结果',
        'test_result': '测试结果',
        'remarks': '备注',
        'create_time': '创建时间',
        'update_time': '更新时间',
        'project': '所属项目',
        'creator': '创建者'
    }
    column_default_sort = ('id', True)
    column_sortable_list = ('id', 'title', 'module', 'case_type', 'case_level', 'create_time', 'update_time')

    def format_creator(self, context, model, name):
        return model.creator.username if model.creator else '未知创建者'
    
    column_formatters = {
        'creator': format_creator
    }
    # 视图行为属性
    page_size = 20
    column_display_actions = True
    create_modal = True
    edit_modal = True
    details_modal = True     
    # 表单配置属性
    form_columns = ('title', 'module', 'case_type', 'case_level', 'preconditions', 'test_steps', 'expected_result', 'test_result', 'remarks', 'project')
    form_overrides = {
        'case_type': SelectField,
        'case_level': SelectField,
        'test_result': SelectField
    }
    form_args = {
        'title': {
            'label': '用例标题',
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入用例标题'}
        },
        'module': {
            'label': '所属模块',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入所属模块'}
        },
        'case_type': {
            'label': '用例类型',            
            'validators': [DataRequired()],
            'choices': [('功能测试', '功能测试'), ('性能测试', '性能测试'),('兼容性测试','兼容性测试')]
        },
        'case_level': {
            'label': '用例等级',            
            'validators': [DataRequired()],
            'choices': [('P0', 'P0'), ('P1', 'P1'), ('P2', 'P2'), ('P3', 'P3')]
        },
        'preconditions': {
            'label': '前置条件',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入前置条件'}
        },
        'test_steps': {
            'label': '测试步骤',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入测试步骤'}
        },
        'expected_result': {
            'label': '预期结果',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入预期结果'}
        },
        'test_result': {
            'label': '测试结果',            
            'validators': [DataRequired()],
            'choices': [('pass', '通过'), ('fail', '失败'), ('not_run', '未执行')]
        },
        'remarks': {
            'label': '备注',       
            'render_kw': {'placeholder': '请输入备注'}
        },
        'project': {
            'label': '所属项目',            
            'validators': [DataRequired()],
            'render_kw': {'placeholder': '请输入所属项目'}
        }
    }


 

def init_admin(app):

    admin = Admin(app, name='后台管理', url='/admin/', index_view=InnoAdminIndexView(), base_template='admin/master.html', template_mode='bootstrap4')  # 创建Admin实例     
    admin.add_view(UserModelView(User, db.session, name='用户管理', endpoint='admin_user'))  
    admin.add_view(RoleModelView(Role, db.session, name='角色管理', endpoint='admin_role'))  
    admin.add_view(ProjectModelView(Project, db.session, name='项目管理', endpoint='admin_project')) 
    admin.add_view(TestCaseModelView(TestCase, db.session, name='用例管理', endpoint='admin_testcase')) 
    
    
     
