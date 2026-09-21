from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Teacher, User, ClassModel, Section, Subject, TeacherAssignment
from app.utils.decorators import role_required
from app.utils.helpers import save_upload_file

teacher_bp = Blueprint('teacher', __name__)


@teacher_bp.route('/')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def index():
    dept = request.args.get('dept', '')
    query = Teacher.query
    if dept:
        query = query.filter_by(department=dept)
    teachers = query.order_by(Teacher.employee_id.asc()).all()
    departments = db.session.query(Teacher.department).distinct().all()
    dept_list = [d[0] for d in departments if d[0]]
    return render_template('dashboard/teachers/list.html', teachers=teachers, departments=dept_list, selected_dept=dept)


@teacher_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def add():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        emp_id = request.form.get('employee_id')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        designation = request.form.get('designation')
        department = request.form.get('department')
        qualification = request.form.get('qualification')
        experience = request.form.get('experience_years', type=int, default=0)
        bio = request.form.get('bio', '')
        username = request.form.get('username')
        password = request.form.get('password', 'teacher123')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('teacher.add'))

        if Teacher.query.filter_by(employee_id=emp_id).first():
            flash('Employee ID already exists.', 'danger')
            return redirect(url_for('teacher.add'))

        photo_file = request.files.get('photo')
        photo_path = save_upload_file(photo_file, subfolder='photos') or 'default_teacher.png'

        user = User(username=username, email=email, role='Teacher')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        teacher = Teacher(
            user_id=user.id,
            employee_id=emp_id,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            email=email,
            phone=phone,
            designation=designation,
            department=department,
            qualification=qualification,
            experience_years=experience,
            profile_photo=photo_path,
            bio=bio
        )
        db.session.add(teacher)
        db.session.commit()

        flash(f'Teacher {teacher.full_name} created successfully.', 'success')
        return redirect(url_for('teacher.index'))

    return render_template('dashboard/teachers/form.html', teacher=None)


@teacher_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def edit(id):
    teacher = Teacher.query.get_or_404(id)

    if request.method == 'POST':
        teacher.first_name = request.form.get('first_name')
        teacher.last_name = request.form.get('last_name')
        teacher.gender = request.form.get('gender')
        teacher.email = request.form.get('email')
        teacher.phone = request.form.get('phone')
        teacher.designation = request.form.get('designation')
        teacher.department = request.form.get('department')
        teacher.qualification = request.form.get('qualification')
        teacher.experience_years = request.form.get('experience_years', type=int)
        teacher.bio = request.form.get('bio')

        photo_file = request.files.get('photo')
        if photo_file and photo_file.filename:
            new_photo = save_upload_file(photo_file, subfolder='photos')
            if new_photo:
                teacher.profile_photo = new_photo

        db.session.commit()
        flash(f'Teacher {teacher.full_name} updated successfully.', 'success')
        return redirect(url_for('teacher.index'))

    return render_template('dashboard/teachers/form.html', teacher=teacher)


@teacher_bp.route('/<int:id>/assign', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def assign(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        class_id = request.form.get('class_id', type=int)
        section_id = request.form.get('section_id', type=int)
        subject_id = request.form.get('subject_id', type=int)

        if class_id and subject_id:
            assignment = TeacherAssignment(
                teacher_id=teacher.id,
                class_id=class_id,
                section_id=section_id if section_id else None,
                subject_id=subject_id
            )
            db.session.add(assignment)
            db.session.commit()
            flash('Assignment added successfully.', 'success')

        return redirect(url_for('teacher.assign', id=teacher.id))

    classes = ClassModel.query.all()
    sections = Section.query.all()
    subjects = Subject.query.all()
    assignments = teacher.assignments.all()
    return render_template('dashboard/teachers/assign.html', teacher=teacher, classes=classes, sections=sections, subjects=subjects, assignments=assignments)


@teacher_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def delete(id):
    teacher = Teacher.query.get_or_404(id)
    user = teacher.user
    db.session.delete(teacher)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Teacher deleted successfully.', 'success')
    return redirect(url_for('teacher.index'))
