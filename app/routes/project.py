from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, TestCase
from app.forms import ProjectForm


project_bp = Blueprint('project', __name__, url_prefix='/project')


# 创建项目
@project_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, description=form.description.data, creator_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('项目创建成功！', 'success')
        return redirect(url_for('main.index'))
    return render_template('projects/new.html', form=form)

# 项目详情页
@project_bp.route('/<int:project_id>')
@login_required
def project_details(project_id):
    project = Project.query.get_or_404(project_id)    
    test_cases = TestCase.query.filter_by(project_id=project_id).all()
    return render_template('projects/detail.html', project=project, testcases=test_cases)


# 编辑项目
@project_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)   

    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash('项目保存成功！','success')
        return redirect(url_for('project.project_details', project_id=project.id))
    return render_template('projects/edit.html', form=form, project=project)


# 删除项目
@project_bp.route('/<int:project_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):    
    project = Project.query.get_or_404(project_id)
    # 删除关联的测试用例
    TestCase.query.filter_by(project_id=project_id).delete()
   
    # 删除项目
    db.session.delete(project)
    db.session.commit()
    flash('已删除项目！','warning')
    return redirect(url_for('main.index'))

