from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User
import re


# 注册表单
class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)], render_kw={'placeholder': '请输入3-20位的用户名'})
    email = StringField('邮箱', validators=[DataRequired(), Email(message='请输入有效的邮箱地址')], render_kw={'placeholder': '请输入有效的邮箱地址'})
    password = PasswordField('密码', 
                            validators=[DataRequired(),
                            Length(min=8, message="密码至少8位"),  # 密码长度限制
                            Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}", message="密码必须包含大写字母、小写字母、数字和特殊字符")],  # 密码复杂度限制
                            render_kw={'placeholder': '密码至少8位且必须包含大小写字母、数字和特殊字符'})
    confirm_password = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='密码不匹配')], render_kw={'placeholder': '请再次输入密码'})
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被注册，请选择其他用户名。')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('该邮箱已被注册，请选择其他邮箱。')


# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default=False)
    submit = SubmitField('登录')


# 项目表单
class ProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired()])
    description = TextAreaField('项目描述', validators=[DataRequired()])
    submit = SubmitField('创建项目')


# 测试用例表单
class TestCaseForm(FlaskForm):
    title = StringField('用例标题', validators=[DataRequired()])
    module = StringField('用例模块', validators=[DataRequired()])
    case_type = SelectField('用例类型', validators=[DataRequired()], choices=[('功能测试', '功能测试'), ('性能测试', '性能测试'), ('兼容性测试', '兼容性测试')])
    case_level = SelectField('用例等级', validators=[DataRequired()], choices=[('P0', '关键'), ('P1', '重要'), ('P2', '次要'), ('P3', '一般')])
    preconditions = TextAreaField('前置条件', validators=[DataRequired()])
    test_steps = TextAreaField('测试步骤', validators=[DataRequired()])
    expected_result = TextAreaField('预期结果', validators=[DataRequired()])
    test_result = SelectField('测试结果', validators=[DataRequired()], choices=[('Pass', '通过'), ('Fail', '失败'), ('Not_run', '未执行')])
    remarks = TextAreaField('备注')
    submit = SubmitField('保存用例')