from flask import Flask, Blueprint, render_template, redirect, url_for, flash, request,  abort
from flask_login import login_user, logout_user, current_user
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Role
import re
from datetime import timedelta
from app.utils.helper import generate_fs_uniquifier


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('登录失败，请检查用户名和密码是否正确', category='error')
            return redirect(url_for('auth.login'))
        elif user.active == False:
            flash('用户未激活，请联系管理员', category='error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data, duration=timedelta(hours=1))  # 1 hour session duration
        flash('登录成功', category='success')

        # 获取next参数的值
        next_page = request.args.get('next')        
        # 依据 next 变量的值来决定重定向的目标页面
        return redirect(next_page or url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # confirm_password = form.confirm_password.data     
        
        # 注册时默认分配普通用户角色
        default_role = Role.query.filter_by(name='user').first()

        # 创建新用户
        user = User(username=username, email=email, active=True, role=default_role, fs_uniquifier=generate_fs_uniquifier())
        user.set_password(password)        

        db.session.add(user)
        db.session.commit()
        
        flash('注册成功，请重新登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)
    

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('您已退出登录', category='info')
    return redirect(url_for('main.index'))