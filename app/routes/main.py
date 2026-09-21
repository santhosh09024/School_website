from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app.extensions import db
from app.models import (
    Teacher, Student, ClassModel, Notice, Event, GalleryAlbum,
    GalleryImage, Document, AdmissionApplication, ContactMessage,
    Examination, Mark, Subject
)
from app.utils.helpers import generate_application_number

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    latest_notices = Notice.query.filter_by(is_published=True).order_by(Notice.created_at.desc()).limit(5).all()
    upcoming_events = Event.query.filter_by(is_upcoming=True).order_by(Event.event_date.asc()).limit(3).all()
    recent_gallery = GalleryAlbum.query.order_by(GalleryAlbum.created_at.desc()).limit(4).all()
    total_students = Student.query.count()
    total_teachers = Teacher.query.count()
    total_classes = ClassModel.query.count()

    return render_template(
        'public/index.html',
        notices=latest_notices,
        events=upcoming_events,
        albums=recent_gallery,
        stats={
            'students': total_students if total_students > 0 else 1250,
            'teachers': total_teachers if total_teachers > 0 else 85,
            'classes': total_classes if total_classes > 0 else 24,
            'pass_rate': '99.4%'
        }
    )


@main_bp.route('/about')
def about():
    teachers_count = Teacher.query.count()
    return render_template('public/about.html', teachers_count=teachers_count)


@main_bp.route('/academics')
def academics():
    classes = ClassModel.query.all()
    return render_template('public/academics.html', classes=classes)


@main_bp.route('/faculty')
def faculty():
    department = request.args.get('dept', '')
    query = Teacher.query
    if department:
        query = query.filter_by(department=department)
    teachers = query.all()
    departments = db.session.query(Teacher.department).distinct().all()
    dept_list = [d[0] for d in departments if d[0]]
    return render_template('public/faculty.html', teachers=teachers, departments=dept_list, selected_dept=department)


@main_bp.route('/admissions', methods=['GET', 'POST'])
def admissions():
    if request.method == 'POST':
        try:
            student_name = request.form.get('student_name')
            dob_str = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            class_applying = request.form.get('class_applying')
            parent_name = request.form.get('parent_name')
            father_name = request.form.get('father_name', '')
            mother_name = request.form.get('mother_name', '')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            previous_school = request.form.get('previous_school', '')
            previous_class = request.form.get('previous_class', '')
            academic_details = request.form.get('academic_details', '')

            dob = date.fromisoformat(dob_str) if dob_str else date(2010, 1, 1)
            app_no = generate_application_number()

            application = AdmissionApplication(
                application_number=app_no,
                student_name=student_name,
                date_of_birth=dob,
                gender=gender,
                class_applying=class_applying,
                parent_name=parent_name,
                father_name=father_name,
                mother_name=mother_name,
                phone=phone,
                email=email,
                address=address,
                previous_school=previous_school,
                previous_class=previous_class,
                academic_details=academic_details,
                status='Pending'
            )
            db.session.add(application)
            db.session.commit()

            flash(f'Application submitted successfully! Your Application Number is: {app_no}. Please save this for tracking.', 'success')
            return redirect(url_for('main.admissions', app_no=app_no))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {str(e)}', 'danger')

    app_no = request.args.get('app_no', '')
    tracked_app = None
    if request.args.get('search_app_no'):
        search_no = request.args.get('search_app_no').strip()
        tracked_app = AdmissionApplication.query.filter_by(application_number=search_no).first()
        if not tracked_app:
            flash(f'No application found with number {search_no}.', 'warning')

    classes = ClassModel.query.all()
    return render_template('public/admissions.html', classes=classes, app_no=app_no, tracked_app=tracked_app)


@main_bp.route('/student-life')
def student_life():
    return render_template('public/student_life.html')


@main_bp.route('/notices')
def notices():
    query = request.args.get('q', '')
    notices_query = Notice.query.filter_by(is_published=True)
    if query:
        notices_query = notices_query.filter(Notice.title.contains(query) | Notice.content.contains(query))
    all_notices = notices_query.order_by(Notice.created_at.desc()).all()
    return render_template('public/notices.html', notices=all_notices, query=query)


@main_bp.route('/events')
def events():
    upcoming = Event.query.filter_by(is_upcoming=True).order_by(Event.event_date.asc()).all()
    past = Event.query.filter_by(is_upcoming=False).order_by(Event.event_date.desc()).all()
    return render_template('public/events.html', upcoming_events=upcoming, past_events=past)


@main_bp.route('/gallery')
def gallery():
    albums = GalleryAlbum.query.all()
    all_images = GalleryImage.query.order_by(GalleryImage.uploaded_at.desc()).all()
    return render_template('public/gallery.html', albums=albums, images=all_images)


@main_bp.route('/downloads')
def downloads():
    documents = Document.query.order_by(Document.uploaded_at.desc()).all()
    return render_template('public/downloads.html', documents=documents)


@main_bp.route('/results', methods=['GET', 'POST'])
def results():
    search_performed = False
    student = None
    exam_marks = []
    total_obtained = 0
    total_max = 0
    overall_percentage = 0.0
    overall_grade = 'N/A'

    if request.method == 'POST':
        search_performed = True
        identifier = request.form.get('identifier', '').strip()  # Student ID or Admission No or Roll No
        dob_str = request.form.get('date_of_birth', '').strip()

        if identifier:
            student = Student.query.filter(
                (Student.admission_number == identifier) |
                (Student.roll_number == identifier)
            ).first()

            if student and dob_str:
                try:
                    dob = date.fromisoformat(dob_str)
                    if student.date_of_birth != dob:
                        student = None
                        flash('Date of birth does not match student records.', 'danger')
                except ValueError:
                    student = None
                    flash('Invalid Date of Birth format.', 'danger')

            if student:
                latest_exam = Examination.query.filter_by(class_id=student.class_id, is_published=True).order_by(Examination.start_date.desc()).first()
                if latest_exam:
                    exam_marks = Mark.query.filter_by(examination_id=latest_exam.id, student_id=student.id).all()
                    if exam_marks:
                        total_obtained = sum(m.total_marks for m in exam_marks)
                        total_max = len(exam_marks) * 100
                        overall_percentage = round((total_obtained / total_max) * 100, 2) if total_max > 0 else 0
                        if overall_percentage >= 90: overall_grade = 'A+'
                        elif overall_percentage >= 80: overall_grade = 'A'
                        elif overall_percentage >= 70: overall_grade = 'B'
                        elif overall_percentage >= 60: overall_grade = 'C'
                        elif overall_percentage >= 50: overall_grade = 'D'
                        else: overall_grade = 'F'
            else:
                if not dob_str:
                    flash('Student record not found. Please double-check Admission/Roll Number.', 'warning')

    return render_template(
        'public/results.html',
        search_performed=search_performed,
        student=student,
        exam_marks=exam_marks,
        total_obtained=total_obtained,
        total_max=total_max,
        overall_percentage=overall_percentage,
        overall_grade=overall_grade
    )


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if name and email and subject and message:
            msg = ContactMessage(name=name, email=email, phone=phone, subject=subject, message=message)
            db.session.add(msg)
            db.session.commit()
            flash('Thank you! Your message has been sent to our admissions office. We will reply shortly.', 'success')
            return redirect(url_for('main.contact'))
        else:
            flash('Please fill in all required fields.', 'danger')

    return render_template('public/contact.html')


@main_bp.route('/faq')
def faq():
    return render_template('public/pages.html', page_type='faq')


@main_bp.route('/privacy-policy')
def privacy():
    return render_template('public/pages.html', page_type='privacy')


@main_bp.route('/terms')
def terms():
    return render_template('public/pages.html', page_type='terms')
