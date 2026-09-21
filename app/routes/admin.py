from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models import (
    Student, Teacher, Parent, ClassModel, AdmissionApplication,
    Attendance, FeePayment, Examination, ContactMessage, SchoolSetting,
    Mark
)
from app.utils.decorators import role_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    today = date.today()

    # Role specific redirection / views
    if current_user.role == 'Teacher':
        teacher = current_user.teacher_profile
        assigned_classes = teacher.assignments.all() if teacher else []
        return render_template('dashboard/teacher_dashboard.html', teacher=teacher, assignments=assigned_classes)

    elif current_user.role == 'Student':
        student = current_user.student_profile
        recent_marks = Mark.query.filter_by(student_id=student.id).limit(5).all() if student else []
        attendances = Attendance.query.filter_by(student_id=student.id).order_by(Attendance.date.desc()).limit(10).all() if student else []
        return render_template('dashboard/student_dashboard.html', student=student, marks=recent_marks, attendances=attendances)

    elif current_user.role == 'Parent':
        parent = current_user.parent_profile
        children = parent.students.all() if parent else []
        return render_template('dashboard/parent_dashboard.html', parent=parent, children=children)

    # General Admin / Super Admin / Principal Dashboard
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_parents = Parent.query.count()
    total_classes = ClassModel.query.count()
    pending_admissions = AdmissionApplication.query.filter_by(status='Pending').count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()

    today_attendance_records = Attendance.query.filter_by(date=today).all()
    present_today = sum(1 for a in today_attendance_records if a.status == 'Present')
    total_today = len(today_attendance_records)
    attendance_pct = round((present_today / total_today) * 100, 1) if total_today > 0 else 96.5

    recent_applications = AdmissionApplication.query.order_by(AdmissionApplication.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()

    return render_template(
        'dashboard/index.html',
        metrics={
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_parents': total_parents,
            'total_classes': total_classes,
            'pending_admissions': pending_admissions,
            'unread_messages': unread_messages,
            'today_attendance_pct': attendance_pct
        },
        recent_applications=recent_applications,
        recent_messages=recent_messages
    )


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def settings():
    if request.method == 'POST':
        setting_keys = ['school_name', 'tagline', 'address', 'phone', 'email', 'office_hours', 'principal_name', 'chairman_name', 'academic_year', 'footer_text']
        for key in setting_keys:
            val = request.form.get(key)
            if val is not None:
                setting = SchoolSetting.query.filter_by(key=key).first()
                if setting:
                    setting.value = val
                else:
                    setting = SchoolSetting(key=key, value=val, label=key.replace('_', ' ').title())
                    db.session.add(setting)
        db.session.commit()
        flash('School settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    settings_list = SchoolSetting.query.all()
    settings_dict = {s.key: s.value for s in settings_list}
    return render_template('dashboard/settings.html', settings=settings_dict)
