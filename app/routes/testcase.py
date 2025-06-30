from flask import Flask, render_template, redirect, url_for, flash, request, Blueprint, abort
from flask_login import login_required, current_user
from app import db
from app.models import Project, TestCase
from app.forms import TestCaseForm

testcase_bp = Blueprint('testcase', __name__, url_prefix='/testcases')

# 新增测试用例
@testcase_bp.route('/<int:project_id>/new', methods=['GET', 'POST'])
@login_required
def new_testcase(project_id):
    project = Project.query.get_or_404(project_id)   
    form = TestCaseForm()
    if form.validate_on_submit():
        test_case = TestCase(            
            title=form.title.data,
            module=form.module.data,
            case_type=form.case_type.data,
            case_level=form.case_level.data,
            preconditions=form.preconditions.data,
            test_steps=form.test_steps.data,
            expected_result=form.expected_result.data,
            test_result=form.test_result.data,
            remarks=form.remarks.data,
            project_id=project_id,  # 关联项目ID 
            creator_id=current_user.id  # 关联创建者ID 
        )    
        db.session.add(test_case)
        db.session.commit()
        flash('测试用例创建成功！', 'success')
        return redirect(url_for('project.project_details', project_id=project_id))
    return render_template('testcases/new.html', form=form, project=project)

# 查看测试用例详情
@testcase_bp.route('/<int:testcase_id>/details')
@login_required
def testcase_details(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)
    project = Project.query.get_or_404(test_case.project_id)  # 获取项目信息
    return render_template('testcases/detail.html', testcase=test_case, project=project)

# 编辑测试用例
@testcase_bp.route('/<int:testcase_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testcase(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)
    project_id = test_case.project_id  # 获取项目ID
    form = TestCaseForm(obj=test_case)
    if form.validate_on_submit():
        test_case.title = form.title.data
        test_case.module = form.module.data
        test_case.case_type = form.case_type.data
        test_case.case_level = form.case_level.data
        test_case.preconditions = form.preconditions.data
        test_case.test_steps = form.test_steps.data
        test_case.expected_result = form.expected_result.data
        test_case.test_result = form.test_result.data
        test_case.remarks = form.remarks.data
        db.session.commit()
        flash('测试用例更新成功！','info')
        return redirect(url_for('project.project_details', project_id=project_id))
    return render_template('testcases/edit.html', form=form, testcase=test_case, project_id=project_id)


# 删除测试用例
@testcase_bp.route('/<int:testcase_id>/delete', methods=['POST'])
@login_required
def delete_testcase(testcase_id):
    test_case = TestCase.query.get_or_404(testcase_id)  # 获取测试用例信息
    project_id = test_case.project_id  # 获取项目ID
    db.session.delete(test_case)
    db.session.commit()
    flash('已删除指定测试用例！','info')
    
    if project_id:
        return redirect(url_for('project.project_details', project_id=project_id))
    else:
        return redirect(url_for('main.index'))
    








