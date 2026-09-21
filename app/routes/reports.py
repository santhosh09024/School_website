import csv
import io
from flask import Blueprint, render_template, request, Response
from flask_login import login_required
from app.models import Student, Attendance, FeePayment, Examination, Mark, Teacher
from app.utils.decorators import role_required

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def index():
    report_type = request.args.get('type', 'students')

    if report_type == 'attendance':
        data = Attendance.query.order_by(Attendance.date.desc()).limit(200).all()
    elif report_type == 'fees':
        data = FeePayment.query.order_by(FeePayment.payment_date.desc()).limit(200).all()
    elif report_type == 'exams':
        data = Mark.query.limit(200).all()
    elif report_type == 'teachers':
        data = Teacher.query.all()
    else:
        data = Student.query.all()

    return render_template('dashboard/reports/index.html', report_type=report_type, data=data)


@reports_bp.route('/export')
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def export():
    report_type = request.args.get('type', 'students')
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == 'attendance':
        writer.writerow(['Date', 'Student Name', 'Class', 'Status', 'Remarks'])
        records = Attendance.query.order_by(Attendance.date.desc()).all()
        for r in records:
            writer.writerow([r.date, r.student_obj.full_name if r.student_obj else '', r.student_obj.class_obj.name if r.student_obj and r.student_obj.class_obj else '', r.status, r.remarks])

    elif report_type == 'fees':
        writer.writerow(['Receipt No', 'Student Name', 'Amount Paid', 'Pending', 'Payment Mode', 'Date', 'Status'])
        payments = FeePayment.query.order_by(FeePayment.payment_date.desc()).all()
        for p in payments:
            writer.writerow([p.receipt_number, p.student_obj.full_name if p.student_obj else '', p.amount_paid, p.pending_amount, p.payment_mode, p.payment_date, p.status])

    elif report_type == 'exams':
        writer.writerow(['Exam', 'Student Name', 'Subject', 'Total Marks', 'Percentage', 'Grade', 'Pass/Fail'])
        marks = Mark.query.all()
        for m in marks:
            writer.writerow([m.examination_obj.title if m.examination_obj else '', m.student_obj.full_name if m.student_obj else '', m.subject_obj.name if m.subject_obj else '', m.total_marks, m.percentage, m.grade, 'PASS' if m.is_pass else 'FAIL'])

    else:
        writer.writerow(['Admission No', 'Roll No', 'Name', 'Gender', 'Class', 'Phone'])
        students = Student.query.all()
        for s in students:
            writer.writerow([s.admission_number, s.roll_number, s.full_name, s.gender, s.class_obj.name if s.class_obj else '', s.phone])

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={report_type}_report.csv'
    return response
