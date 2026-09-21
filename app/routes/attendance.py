from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Attendance, Student, ClassModel, Section
from app.utils.decorators import role_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal', 'Teacher')
def mark():
    selected_class = request.args.get('class_id', type=int)
    selected_section = request.args.get('section_id', type=int)
    date_str = request.args.get('date', date.today().isoformat())
    target_date = date.fromisoformat(date_str)

    if request.method == 'POST':
        c_id = request.form.get('class_id', type=int)
        s_id = request.form.get('section_id', type=int)
        att_date_str = request.form.get('date')
        att_date = date.fromisoformat(att_date_str) if att_date_str else date.today()

        student_ids = request.form.getlist('student_ids')

        for sid in student_ids:
            st_id = int(sid)
            status_val = request.form.get(f'status_{st_id}', 'Present')
            remarks_val = request.form.get(f'remarks_{st_id}', '')

            # Check existing attendance record for student + date
            existing = Attendance.query.filter_by(student_id=st_id, date=att_date).first()
            if existing:
                existing.status = status_val
                existing.remarks = remarks_val
                existing.recorded_by = current_user.username
            else:
                att = Attendance(
                    student_id=st_id,
                    class_id=c_id,
                    section_id=s_id,
                    date=att_date,
                    status=status_val,
                    remarks=remarks_val,
                    recorded_by=current_user.username
                )
                db.session.add(att)

        db.session.commit()
        flash('Attendance updated successfully!', 'success')
        return redirect(url_for('attendance.mark', class_id=c_id, section_id=s_id, date=att_date.isoformat()))

    classes = ClassModel.query.all()
    sections = Section.query.filter_by(class_id=selected_class).all() if selected_class else []
    students = []
    attendance_map = {}

    if selected_class:
        st_query = Student.query.filter_by(class_id=selected_class)
        if selected_section:
            st_query = st_query.filter_by(section_id=selected_section)
        students = st_query.order_by(Student.roll_number.asc()).all()

        existing_records = Attendance.query.filter(
            Attendance.student_id.in_([s.id for s in students]),
            Attendance.date == target_date
        ).all() if students else []

        for rec in existing_records:
            attendance_map[rec.student_id] = rec

    return render_template(
        'dashboard/attendance/mark.html',
        classes=classes,
        sections=sections,
        students=students,
        selected_class=selected_class,
        selected_section=selected_section,
        target_date=target_date,
        attendance_map=attendance_map
    )


@attendance_bp.route('/report')
@login_required
def report():
    class_id = request.args.get('class_id', type=int)

    stats = {
        'total': Student.query.count(),
        'present': 0,
        'absent': 0,
        'late': 0,
        'leave': 0,
        'percentage': 0.0
    }

    records = []
    if class_id:
        students = Student.query.filter_by(class_id=class_id).all()
        student_ids = [s.id for s in students]
        records = Attendance.query.filter(Attendance.student_id.in_(student_ids)).order_by(Attendance.date.desc()).limit(100).all()

        if records:
            stats['present'] = sum(1 for r in records if r.status == 'Present')
            stats['absent'] = sum(1 for r in records if r.status == 'Absent')
            stats['late'] = sum(1 for r in records if r.status == 'Late')
            stats['leave'] = sum(1 for r in records if r.status == 'Leave')
            stats['percentage'] = round((stats['present'] / len(records)) * 100, 1)

    classes = ClassModel.query.all()
    return render_template('dashboard/attendance/report.html', classes=classes, selected_class=class_id, records=records, stats=stats)
