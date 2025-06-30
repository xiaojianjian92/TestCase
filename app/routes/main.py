from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from app import db
from app.models import Project, TestCase

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # 获取项目列表
    if current_user.is_authenticated:
        project_list = Project.query.all()   
        return render_template('index.html', project_list=project_list)
    else:
        return render_template('index.html')
    
@main_bp.route('/admin')
@login_required
def admin():
    if current_user.role.name == 'admin':  
        return url_for('admin.index')  
    else:
        flash('您没有权限访问此页面', 'error')  
        return redirect(url_for('main.index'))  