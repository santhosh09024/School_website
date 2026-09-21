from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
import csv
import io
from flask_login import login_required
from app.extensions import db
from app.models import Student, User, ClassModel, Section, Parent, AcademicYear
from app.utils.decorators import role_required
from app.utils.helpers import save_upload_file

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
@login_required
@role_required('Super Admin', 'Admin', 'Principal', 'Teacher')
def index():
    search_q = request.args.get('q', '').strip()
    class_id = request.args.get('class_id', type=int)

    query = Student.query
    if search_q:
        query = query.filter(
            (Student.first_name.contains(search_q)) |
            (Student.last_name.contains(search_q)) |
            (Student.admission_number.contains(search_q)) |
            (Student.roll_number.contains(search_q))
        )
    if class_id:
        query = query.filter_by(class_id=class_id)

    students = query.order_by(Student.admission_number.asc()).all()
    classes = ClassModel.query.all()

    return render_template('dashboard/students/list.html', students=students, classes=classes, selected_class=class_id, search_q=search_q)


@student_bp.route('/add', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def add():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        admission_no = request.form.get('admission_number')
        roll_no = request.form.get('roll_number')
        gender = request.form.get('gender')
        dob_str = request.form.get('date_of_birth')
        class_id = request.form.get('class_id', type=int)
        section_id = request.form.get('section_id', type=int)
        parent_id = request.form.get('parent_id', type=int)
        phone = request.form.get('phone', '')
        address = request.form.get('address', '')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password', 'student123')

        # Check username / admission number uniqueness
        if User.query.filter_by(username=username).first():
            flash('Username is already taken.', 'danger')
            return redirect(url_for('student.add'))

        if Student.query.filter_by(admission_number=admission_no).first():
            flash('Admission number already exists.', 'danger')
            return redirect(url_for('student.add'))

        ay = AcademicYear.query.filter_by(is_current=True).first()
        ay_id = ay.id if ay else 1

        # Photo upload
        photo_file = request.files.get('photo')
        photo_path = save_upload_file(photo_file, subfolder='photos') or 'default_student.png'

        user = User(username=username, email=email, role='Student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        student = Student(
            user_id=user.id,
            admission_number=admission_no,
            roll_number=roll_no,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date.fromisoformat(dob_str),
            class_id=class_id,
            section_id=section_id,
            parent_id=parent_id if parent_id else None,
            academic_year_id=ay_id,
            phone=phone,
            address=address,
            photo=photo_path
        )
        db.session.add(student)
        db.session.commit()

        flash(f'Student {student.full_name} added successfully!', 'success')
        return redirect(url_for('student.index'))

    classes = ClassModel.query.all()
    sections = Section.query.all()
    parents = Parent.query.all()
    return render_template('dashboard/students/form.html', student=None, classes=classes, sections=sections, parents=parents)


@student_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def edit(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.roll_number = request.form.get('roll_number')
        student.gender = request.form.get('gender')
        student.class_id = request.form.get('class_id', type=int)
        student.section_id = request.form.get('section_id', type=int)
        student.parent_id = request.form.get('parent_id', type=int) or None
        student.phone = request.form.get('phone', '')
        student.address = request.form.get('address', '')
        student.status = request.form.get('status', 'Active')

        dob_str = request.form.get('date_of_birth')
        if dob_str:
            student.date_of_birth = date.fromisoformat(dob_str)

        photo_file = request.files.get('photo')
        if photo_file and photo_file.filename:
            new_photo = save_upload_file(photo_file, subfolder='photos')
            if new_photo:
                student.photo = new_photo

        db.session.commit()
        flash(f'Student {student.full_name} updated successfully.', 'success')
        return redirect(url_for('student.index'))

    classes = ClassModel.query.all()
    sections = Section.query.all()
    parents = Parent.query.all()
    return render_template('dashboard/students/form.html', student=student, classes=classes, sections=sections, parents=parents)


@student_bp.route('/<int:id>/view')
@login_required
def view(id):
    student = Student.query.get_or_404(id)
    return render_template('dashboard/students/view.html', student=student)


@student_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def delete(id):
    student = Student.query.get_or_404(id)
    user = student.user
    db.session.delete(student)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('student.index'))


@student_bp.route('/export/csv')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def export_csv():
    students = Student.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Admission No', 'Roll No', 'Name', 'Class', 'Section', 'Gender', 'Phone', 'Status'])

    for s in students:
        writer.writerow([
            s.admission_number,
            s.roll_number,
            s.full_name,
            s.class_obj.name if s.class_obj else '',
            s.section_obj.name if s.section_obj else '',
            s.gender,
            s.phone,
            s.status
        ])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=students_export.csv'
    return response
