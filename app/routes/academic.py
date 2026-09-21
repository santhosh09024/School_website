from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import ClassModel, Section, Subject, Timetable, Teacher
from app.utils.decorators import role_required

academic_bp = Blueprint('academic', __name__)


@academic_bp.route('/classes', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def classes():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        category = request.form.get('category', 'Primary')
        description = request.form.get('description', '')

        if ClassModel.query.filter_by(code=code).first():
            flash('Class code already exists.', 'danger')
        else:
            cls = ClassModel(name=name, code=code, category=category, description=description)
            db.session.add(cls)
            db.session.commit()
            flash(f'Class {name} created successfully.', 'success')

        return redirect(url_for('academic.classes'))

    all_classes = ClassModel.query.all()
    return render_template('dashboard/classes/index.html', classes=all_classes)


@academic_bp.route('/sections', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def add_section():
    class_id = request.form.get('class_id', type=int)
    name = request.form.get('name')
    capacity = request.form.get('capacity', type=int, default=40)

    if class_id and name:
        sec = Section(class_id=class_id, name=name, capacity=capacity)
        db.session.add(sec)
        db.session.commit()
        flash(f'Section {name} added.', 'success')

    return redirect(url_for('academic.classes'))


@academic_bp.route('/subjects', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def subjects():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        class_id = request.form.get('class_id', type=int)
        department = request.form.get('department', 'General')
        pass_marks = request.form.get('pass_marks', type=float, default=40.0)
        max_marks = request.form.get('max_marks', type=float, default=100.0)

        if Subject.query.filter_by(code=code).first():
            flash('Subject code already exists.', 'danger')
        else:
            subj = Subject(name=name, code=code, class_id=class_id, department=department, pass_marks=pass_marks, max_marks=max_marks)
            db.session.add(subj)
            db.session.commit()
            flash(f'Subject {name} created.', 'success')

        return redirect(url_for('academic.subjects'))

    all_subjects = Subject.query.all()
    classes = ClassModel.query.all()
    return render_template('dashboard/classes/subjects.html', subjects=all_subjects, classes=classes)


@academic_bp.route('/timetable', methods=['GET', 'POST'])
@login_required
def timetable():
    class_id = request.args.get('class_id', type=int)
    section_id = request.args.get('section_id', type=int)

    if request.method == 'POST':
        c_id = request.form.get('class_id', type=int)
        s_id = request.form.get('section_id', type=int)
        subj_id = request.form.get('subject_id', type=int)
        t_id = request.form.get('teacher_id', type=int)
        day = request.form.get('day_of_week')
        period = request.form.get('period_number', type=int)
        start_t = request.form.get('start_time')
        end_t = request.form.get('end_time')
        room = request.form.get('room_number', '101')

        slot = Timetable(
            class_id=c_id,
            section_id=s_id,
            subject_id=subj_id,
            teacher_id=t_id,
            day_of_week=day,
            period_number=period,
            start_time=start_t,
            end_time=end_t,
            room_number=room
        )
        db.session.add(slot)
        db.session.commit()
        flash('Timetable slot added successfully.', 'success')
        return redirect(url_for('academic.timetable', class_id=c_id, section_id=s_id))

    classes = ClassModel.query.all()
    sections = Section.query.filter_by(class_id=class_id).all() if class_id else []
    subjects = Subject.query.filter_by(class_id=class_id).all() if class_id else []
    teachers = Teacher.query.all()

    timetable_items = []
    if class_id:
        q = Timetable.query.filter_by(class_id=class_id)
        if section_id:
            q = q.filter_by(section_id=section_id)
        timetable_items = q.order_by(Timetable.period_number.asc()).all()

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return render_template(
        'dashboard/classes/timetable.html',
        classes=classes,
        sections=sections,
        subjects=subjects,
        teachers=teachers,
        timetable_items=timetable_items,
        selected_class=class_id,
        selected_section=section_id,
        days=days
    )
