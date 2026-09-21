from datetime import date, datetime, timedelta
from app.extensions import db
from app.models import (
    Role, User, AcademicYear, ClassModel, Section, Subject, Timetable,
    Teacher, TeacherAssignment, Student, Parent, AdmissionApplication,
    Attendance, Examination, ExamSubject, Mark,
    FeeCategory, FeeStructure, FeePayment, Notice, Event, ContactMessage,
    GalleryAlbum, GalleryImage, Document, SchoolSetting
)


def seed_database():
    """Populate database with complete production-grade demo data."""
    # 1. Roles
    roles = ['Super Admin', 'Admin', 'Principal', 'Teacher', 'Student', 'Parent']
    for r_name in roles:
        if not Role.query.filter_by(name=r_name).first():
            db.session.add(Role(name=r_name, description=f'{r_name} role permission'))
    db.session.commit()

    # 2. Academic Years
    curr_ay = AcademicYear.query.filter_by(year_label='2025-2026').first()
    if not curr_ay:
        curr_ay = AcademicYear(
            year_label='2025-2026',
            is_current=True,
            start_date=date(2025, 6, 1),
            end_date=date(2026, 4, 30)
        )
        db.session.add(curr_ay)
        db.session.commit()

    # 3. School Settings
    settings = {
        'school_name': 'EduLead INTERNATIONAL SCHOOL',
        'tagline': 'Nurturing Minds, Shaping Futures',
        'address': '123 Knowledge Parkway, Education City',
        'phone': '+91 98765 43210',
        'email': 'info@eduleadschool.com',
        'office_hours': 'Mon - Sat: 8:00 AM - 4:00 PM',
        'principal_name': 'Dr. Eleanor Vance, Ph.D.',
        'chairman_name': 'Prof. Arthur Pendelton',
        'academic_year': '2025-2026',
        'footer_text': '© 2026 EduLead International School. All Rights Reserved.'
    }
    for k, v in settings.items():
        if not SchoolSetting.query.filter_by(key=k).first():
            db.session.add(SchoolSetting(key=k, value=v, label=k.replace('_', ' ').title()))
    db.session.commit()

    # 4. Create Users (SuperAdmin, Admin, Principal, Teachers, Parents, Students)
    users_data = [
        ('superadmin', 'superadmin@school.com', 'admin123', 'Super Admin'),
        ('admin', 'admin@school.com', 'admin123', 'Admin'),
        ('principal', 'principal@school.com', 'principal123', 'Principal'),
        ('teacher_john', 'john.doe@school.com', 'teacher123', 'Teacher'),
        ('teacher_sarah', 'sarah.connor@school.com', 'teacher123', 'Teacher'),
        ('parent_robert', 'robert.smith@gmail.com', 'parent123', 'Parent'),
        ('student_alex', 'alex.smith@student.com', 'student123', 'Student'),
        ('student_emma', 'emma.watson@student.com', 'student123', 'Student'),
    ]

    user_objs = {}
    for uname, email, pwd, role in users_data:
        u = User.query.filter_by(username=uname).first()
        if not u:
            u = User(username=uname, email=email, role=role)
            u.set_password(pwd)
            db.session.add(u)
            db.session.commit()
        user_objs[uname] = u

    # 5. Classes & Sections
    class_10 = ClassModel.query.filter_by(code='CLS-10').first()
    if not class_10:
        class_10 = ClassModel(name='Class 10', code='CLS-10', category='High School', description='Grade 10 Secondary Education Program')
        class_9 = ClassModel(name='Class 9', code='CLS-9', category='High School', description='Grade 9 Secondary Education Program')
        class_5 = ClassModel(name='Class 5', code='CLS-5', category='Primary', description='Grade 5 Primary Education Program')
        db.session.add_all([class_10, class_9, class_5])
        db.session.commit()

        sec_10a = Section(class_id=class_10.id, name='Section A', capacity=35)
        sec_10b = Section(class_id=class_10.id, name='Section B', capacity=35)
        sec_9a = Section(class_id=class_9.id, name='Section A', capacity=40)
        sec_5a = Section(class_id=class_5.id, name='Section A', capacity=30)
        db.session.add_all([sec_10a, sec_10b, sec_9a, sec_5a])
        db.session.commit()
    else:
        sec_10a = Section.query.filter_by(class_id=class_10.id, name='Section A').first()

    # 6. Subjects
    subj_math = Subject.query.filter_by(code='MATH-10').first()
    if not subj_math:
        subj_math = Subject(name='Mathematics', code='MATH-10', class_id=class_10.id, department='Mathematics', pass_marks=40, max_marks=100)
        subj_sci = Subject(name='Science & Physics', code='SCI-10', class_id=class_10.id, department='Science', pass_marks=40, max_marks=100)
        subj_eng = Subject(name='English Literature', code='ENG-10', class_id=class_10.id, department='English', pass_marks=40, max_marks=100)
        subj_his = Subject(name='World History', code='HIS-10', class_id=class_10.id, department='Social Studies', pass_marks=40, max_marks=100)
        db.session.add_all([subj_math, subj_sci, subj_eng, subj_his])
        db.session.commit()

    # 7. Teachers
    t_john = Teacher.query.filter_by(user_id=user_objs['teacher_john'].id).first()
    if not t_john:
        t_john = Teacher(
            user_id=user_objs['teacher_john'].id,
            employee_id='EMP-1001',
            first_name='John',
            last_name='Doe',
            gender='Male',
            email='john.doe@school.com',
            phone='+1 555-0192',
            designation='Senior Science Teacher',
            department='Science',
            qualification='M.Sc. Physics, B.Ed',
            experience_years=8,
            bio='Passionate about experimental physics and inspiring young minds in STEM fields.'
        )
        t_sarah = Teacher(
            user_id=user_objs['teacher_sarah'].id,
            employee_id='EMP-1002',
            first_name='Sarah',
            last_name='Connor',
            gender='Female',
            email='sarah.connor@school.com',
            phone='+1 555-0198',
            designation='Head of Mathematics',
            department='Mathematics',
            qualification='M.A. Mathematics, Ph.D.',
            experience_years=12,
            bio='Dedicated to making complex mathematical concepts intuitive and enjoyable.'
        )
        db.session.add_all([t_john, t_sarah])
        db.session.commit()

    # 8. Parents
    p_robert = Parent.query.filter_by(user_id=user_objs['parent_robert'].id).first()
    if not p_robert:
        p_robert = Parent(
            user_id=user_objs['parent_robert'].id,
            father_name='Robert Smith',
            mother_name='Catherine Smith',
            occupation='Software Engineer',
            phone='+1 555-8833',
            email='robert.smith@gmail.com',
            address='742 Evergreen Terrace, Knowledge City'
        )
        db.session.add(p_robert)
        db.session.commit()

    # 9. Students
    s_alex = Student.query.filter_by(admission_number='ADM-2025-001').first()
    if not s_alex:
        s_alex = Student(
            user_id=user_objs['student_alex'].id,
            admission_number='ADM-2025-001',
            roll_number='1001',
            first_name='Alex',
            last_name='Smith',
            gender='Male',
            date_of_birth=date(2010, 5, 14),
            class_id=class_10.id,
            section_id=sec_10a.id,
            parent_id=p_robert.id,
            academic_year_id=curr_ay.id,
            phone='+1 555-9901',
            address='742 Evergreen Terrace, Knowledge City',
            admission_date=date(2025, 6, 5)
        )
        s_emma = Student(
            user_id=user_objs['student_emma'].id,
            admission_number='ADM-2025-002',
            roll_number='1002',
            first_name='Emma',
            last_name='Watson',
            gender='Female',
            date_of_birth=date(2010, 8, 22),
            class_id=class_10.id,
            section_id=sec_10a.id,
            parent_id=p_robert.id,
            academic_year_id=curr_ay.id,
            phone='+1 555-9902',
            address='12 Baker Street, Knowledge City',
            admission_date=date(2025, 6, 6)
        )
        db.session.add_all([s_alex, s_emma])
        db.session.commit()

    # 10. Admission Applications
    if not AdmissionApplication.query.filter_by(application_number='ADM-APP-101').first():
        app1 = AdmissionApplication(
            application_number='ADM-APP-101',
            student_name='David Miller',
            date_of_birth=date(2011, 3, 10),
            gender='Male',
            class_applying='Class 9',
            parent_name='George Miller',
            father_name='George Miller',
            mother_name='Sarah Miller',
            phone='+1 555-4422',
            email='george.miller@example.com',
            address='45 Park Avenue, Metro City',
            previous_school='St. Jude Academy',
            previous_class='Class 8',
            academic_details='Scored 92% in Grade 8 Final Board Exams.',
            status='Pending'
        )
        db.session.add(app1)
        db.session.commit()

    # 11. Timetable
    if not Timetable.query.filter_by(class_id=class_10.id, day_of_week='Monday', period_number=1).first():
        tt1 = Timetable(class_id=class_10.id, section_id=sec_10a.id, subject_id=subj_math.id, teacher_id=t_sarah.id, day_of_week='Monday', period_number=1, start_time='08:30 AM', end_time='09:15 AM', room_number='Room 201')
        tt2 = Timetable(class_id=class_10.id, section_id=sec_10a.id, subject_id=subj_sci.id, teacher_id=t_john.id, day_of_week='Monday', period_number=2, start_time='09:15 AM', end_time='10:00 AM', room_number='Lab 1')
        tt3 = Timetable(class_id=class_10.id, section_id=sec_10a.id, subject_id=subj_eng.id, teacher_id=t_john.id, day_of_week='Monday', period_number=3, start_time='10:15 AM', end_time='11:00 AM', room_number='Room 201')
        db.session.add_all([tt1, tt2, tt3])
        db.session.commit()

    # 12. Attendance records
    today = date.today()
    for offset in range(5):
        past_date = today - timedelta(days=offset)
        if past_date.weekday() < 5:  # Monday to Friday
            if not Attendance.query.filter_by(student_id=s_alex.id, date=past_date).first():
                db.session.add(Attendance(student_id=s_alex.id, class_id=class_10.id, section_id=sec_10a.id, date=past_date, status='Present', remarks='On time', recorded_by='John Doe'))
                db.session.add(Attendance(student_id=s_emma.id, class_id=class_10.id, section_id=sec_10a.id, date=past_date, status='Present' if offset != 1 else 'Late', remarks='On time' if offset != 1 else 'Traffic delay', recorded_by='John Doe'))
    db.session.commit()

    # 13. Examination & Marks
    exam = Examination.query.filter_by(title='Mid-Term Board Examination 2025').first()
    if not exam:
        exam = Examination(
            title='Mid-Term Board Examination 2025',
            academic_year_id=curr_ay.id,
            class_id=class_10.id,
            start_date=date(2025, 10, 10),
            end_date=date(2025, 10, 20),
            is_published=True
        )
        db.session.add(exam)
        db.session.commit()

        # Add exam subject & marks
        es_math = ExamSubject(examination_id=exam.id, subject_id=subj_math.id, max_marks=100, pass_marks=40, exam_date=date(2025, 10, 10))
        es_sci = ExamSubject(examination_id=exam.id, subject_id=subj_sci.id, max_marks=100, pass_marks=40, exam_date=date(2025, 10, 12))
        db.session.add_all([es_math, es_sci])
        db.session.commit()

        m1 = Mark(examination_id=exam.id, student_id=s_alex.id, subject_id=subj_math.id, internal_marks=18, theory_marks=70, practical_marks=0, total_marks=88, percentage=88.0, grade='A', is_pass=True, remarks='Excellent problem solving')
        m2 = Mark(examination_id=exam.id, student_id=s_alex.id, subject_id=subj_sci.id, internal_marks=19, theory_marks=55, practical_marks=20, total_marks=94, percentage=94.0, grade='A+', is_pass=True, remarks='Outstanding lab work')
        m3 = Mark(examination_id=exam.id, student_id=s_emma.id, subject_id=subj_math.id, internal_marks=20, theory_marks=72, practical_marks=0, total_marks=92, percentage=92.0, grade='A+', is_pass=True, remarks='Top scorer')
        db.session.add_all([m1, m2, m3])
        db.session.commit()

    # 14. Fee Categories & Structure
    fc_tui = FeeCategory.query.filter_by(name='Tuition Fee').first()
    if not fc_tui:
        fc_tui = FeeCategory(name='Tuition Fee', description='Term Tuition & Academic Fee', default_amount=1500.0)
        fc_adm = FeeCategory(name='Admission Fee', description='One time registration charge', default_amount=500.0)
        fc_lab = FeeCategory(name='Laboratory & Library Fee', description='Lab usage & digital library access', default_amount=300.0)
        db.session.add_all([fc_tui, fc_adm, fc_lab])
        db.session.commit()

        fs1 = FeeStructure(academic_year_id=curr_ay.id, class_id=class_10.id, fee_category_id=fc_tui.id, amount=1500.0, due_date=date(2025, 11, 30))
        db.session.add(fs1)
        db.session.commit()

        fp1 = FeePayment(student_id=s_alex.id, fee_structure_id=fs1.id, receipt_number='REC-2025-001', transaction_id='TXN-998811', amount_paid=1500.0, pending_amount=0.0, payment_mode='Online', payment_date=date(2025, 11, 10), status='Paid', remarks='Term 1 Paid in full')
        db.session.add(fp1)
        db.session.commit()

    # 15. Notices & Events
    if not Notice.query.filter_by(title='Annual Sports & Cultural Meet 2026 Announcement').first():
        n1 = Notice(
            title='Annual Sports & Cultural Meet 2026 Announcement',
            content='We are thrilled to announce that the Annual Sports and Cultural Fest will be held from March 15 to March 18. All students are invited to register for athletic track events and stage performances.',
            target_role='All',
            is_published=True,
            publish_date=date.today(),
            expiry_date=date.today() + timedelta(days=30)
        )
        n2 = Notice(
            title='Parent-Teacher Conference (PTC) Schedule',
            content='The Term 2 Parent-Teacher Conference for High School classes will take place on Saturday at 9:00 AM. Attendance is mandatory for academic performance review.',
            target_role='Parent',
            is_published=True,
            publish_date=date.today(),
            expiry_date=date.today() + timedelta(days=15)
        )
        db.session.add_all([n1, n2])
        db.session.commit()

    if not Event.query.filter_by(title='Science & Innovation Fair 2026').first():
        ev1 = Event(
            title='Science & Innovation Fair 2026',
            description='Students will showcase groundbreaking robotics, AI models, green energy solutions, and chemistry projects before external industry judges.',
            event_date=date.today() + timedelta(days=12),
            event_time='10:00 AM - 04:00 PM',
            location='Main Campus Quadrangle',
            registration_link='https://apexschool.edu/register-science-fair',
            is_upcoming=True
        )
        ev2 = Event(
            title='Inter-School Debate Championship',
            description='Debating teams from 15 regional schools compete on modern global policy and climate ethics topics.',
            event_date=date.today() + timedelta(days=25),
            event_time='09:00 AM - 02:00 PM',
            location='Auditorium Hall B',
            is_upcoming=True
        )
        db.session.add_all([ev1, ev2])
        db.session.commit()

    # 16. Gallery & Documents
    if not GalleryAlbum.query.filter_by(title='Annual Academic Awards Night').first():
        alb = GalleryAlbum(title='Annual Academic Awards Night', description='Celebrating student academic excellence and leadership trophies.')
        db.session.add(alb)
        db.session.commit()

    if not Document.query.filter_by(title='Official School Prospectus 2025-2026').first():
        doc1 = Document(title='Official School Prospectus 2025-2026', category='Prospectus', file_path='documents/prospectus_2025.pdf', file_size='2.4 MB', description='Comprehensive guide to academic curriculum, campus facilities, and admission criteria.')
        doc2 = Document(title='Class 10 Syllabus & Exam Pattern', category='Syllabus', file_path='documents/syllabus_class10.pdf', file_size='1.1 MB', description='Detailed subject-wise breakdown for Grade 10 final examinations.')
        db.session.add_all([doc1, doc2])
        db.session.commit()

    # 17. Contact Messages
    if not ContactMessage.query.filter_by(email='parent.inquiry@gmail.com').first():
        msg1 = ContactMessage(name='Sarah Jenkins', email='parent.inquiry@gmail.com', phone='+1 555-7711', subject='Inquiry regarding Grade 6 admissions', message='Hello, I would like to schedule a campus tour for my daughter applying to Grade 6 next term.', is_read=False)
        db.session.add(msg1)
        db.session.commit()

    print("[SUCCESS] Database successfully seeded with demo accounts and data!")
