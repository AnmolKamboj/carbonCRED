# Flask Routes for Approval System

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import User

approval = Blueprint('approval', __name__)

@approval.route('/bank/pending-employers')
@login_required
def pending_employers():
    if current_user.role != 'bank':
        return redirect(url_for('dashboard'))
    pending_employers = User.query.filter_by(role='employer', approved=False).all()
    return render_template('bank/pending_employers.html', pending_employers=pending_employers)

@approval.route('/bank/approve-employer/<int:user_id>', methods=['POST'])
@login_required
def approve_employer(user_id):
    if current_user.role != 'bank':
        return redirect(url_for('dashboard'))
    employer = User.query.get(user_id)
    if employer and employer.role == 'employer':
        employer.approved = True
        db.session.commit()
        flash('Employer approved successfully!', 'success')
    return redirect(url_for('approval.pending_employers'))

@approval.route('/employer/pending-employees')
@login_required
def pending_employees():
    if current_user.role != 'employer':
        return redirect(url_for('dashboard'))
    pending_employees = User.query.filter_by(role='employee', employer_id=current_user.id, approved=False).all()
    return render_template('employer/pending_employees.html', pending_employees=pending_employees)

@approval.route('/employer/approve-employee/<int:user_id>', methods=['POST'])
@login_required
def approve_employee(user_id):
    if current_user.role != 'employer':
        return redirect(url_for('dashboard'))
    employee = User.query.get(user_id)
    if employee and employee.employer_id == current_user.id:
        employee.approved = True
        db.session.commit()
        flash('Employee approved successfully!', 'success')
    return redirect(url_for('approval.manage_employees')) 

@approval.route('/employer/manage-employees')
@login_required
def manage_employees():
    print("👀 Current User:", current_user.username, current_user.id)

    if current_user.role != 'employer':
        return redirect(url_for('dashboard'))

    pending_employees = User.query.filter_by(
        role='employee',
        employer_id=current_user.id,
        approved=False
    ).all()

    approved_employees = User.query.filter_by(
        role='employee',
        employer_id=current_user.id,
        approved=True
    ).all()

    print("🛠 Pending Employees:", pending_employees)
    print("🛠 Approved Employees:", approved_employees)

    return render_template(
        "employer/manage_employees.html",
        pending_employees=pending_employees,
        approved_employees=approved_employees
    )