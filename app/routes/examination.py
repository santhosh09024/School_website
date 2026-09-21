from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import Examination, ExamSubject, Mark, Student, ClassModel, Subject, AcademicYear
from app.utils.decorators import role_required

exam_bp = Blueprint('examination', __name__)


@exam_bp.route('/')
@login_required
def index():
    exams = Examination.query.order_by(Examination.start_date.desc()).all()
    classes = ClassModel.query.all()
    return render_template('dashboard/examinations/list.html', exams=exams, classes=classes)


@exam_bp.route('/create', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal')
def create():
    title = request.form.get('title')
    class_id = request.form.get('class_id', type=int)
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')

    ay = AcademicYear.query.filter_by(is_current=True).first()
    ay_id = ay.id if ay else 1

    if title and class_id:
        exam = Examination(
            title=title,
            academic_year_id=ay_id,
            class_id=class_id,
            start_date=date.fromisoformat(start_date_str),
            end_date=date.fromisoformat(end_date_str),
            is_published=True
        )
        db.session.add(exam)
        db.session.commit()
        flash(f'Examination "{title}" created successfully.', 'success')

    return redirect(url_for('examination.index'))


@exam_bp.route('/<int:exam_id>/marks', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin', 'Principal', 'Teacher')
def marks_entry(exam_id):
    exam = Examination.query.get_or_404(exam_id)
    subject_id = request.args.get('subject_id', type=int)

    subjects = Subject.query.filter_by(class_id=exam.class_id).all()
    students = Student.query.filter_by(class_id=exam.class_id).order_by(Student.roll_number.asc()).all()

    if request.method == 'POST':
        subj_id = request.form.get('subject_id', type=int)
        target_subject = Subject.query.get(subj_id)
        max_m = target_subject.max_marks if target_subject else 100.0
        pass_m = target_subject.pass_marks if target_subject else 40.0

        for s in students:
            int_m = request.form.get(f'internal_{s.id}', type=float, default=0.0)
            th_m = request.form.get(f'theory_{s.id}', type=float, default=0.0)
            prac_m = request.form.get(f'practical_{s.id}', type=float, default=0.0)
            remarks = request.form.get(f'remarks_{s.id}', '')

            existing_mark = Mark.query.filter_by(examination_id=exam.id, student_id=s.id, subject_id=subj_id).first()
            if existing_mark:
                existing_mark.internal_marks = int_m
                existing_mark.theory_marks = th_m
                existing_mark.practical_marks = prac_m
                existing_mark.remarks = remarks
                existing_mark.calculate_grade(max_marks=max_m, pass_marks=pass_m)
            else:
                mark = Mark(
                    examination_id=exam.id,
                    student_id=s.id,
                    subject_id=subj_id,
                    internal_marks=int_m,
                    theory_marks=th_m,
                    practical_marks=prac_m,
                    total_marks=int_m + th_m + prac_m,
                    remarks=remarks
                )
                mark.calculate_grade(max_marks=max_m, pass_marks=pass_m)
                db.session.add(mark)

        db.session.commit()
        flash('Marks saved and grades recalculated successfully.', 'success')
        return redirect(url_for('examination.marks_entry', exam_id=exam.id, subject_id=subj_id))

    marks_map = {}
    if subject_id:
        existing_marks = Mark.query.filter_by(examination_id=exam.id, subject_id=subject_id).all()
        for m in existing_marks:
            marks_map[m.student_id] = m

    return render_template(
        'dashboard/examinations/marks_entry.html',
        exam=exam,
        subjects=subjects,
        students=students,
        selected_subject=subject_id,
        marks_map=marks_map
    )


@exam_bp.route('/<int:exam_id>/student/<int:student_id>/report-card')
@login_required
def report_card(exam_id, student_id):
    exam = Examination.query.get_or_404(exam_id)
    student = Student.query.get_or_404(student_id)
    marks = Mark.query.filter_by(examination_id=exam.id, student_id=student.id).all()

    total_obtained = sum(m.total_marks for m in marks)
    total_max = len(marks) * 100
    pct = round((total_obtained / total_max) * 100, 2) if total_max > 0 else 0.0

    return render_template(
        'dashboard/examinations/report_card.html',
        exam=exam,
        student=student,
        marks=marks,
        total_obtained=total_obtained,
        total_max=total_max,
        percentage=pct
    )
