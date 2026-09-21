import unittest
from datetime import date
from app import create_app, db
from app.models import ClassModel, Section, Student, User, AcademicYear, Mark, Examination, Subject, Role


class CRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        role = Role.query.filter_by(name='Student').first()
        if not role:
            role = Role(name='Student', description='Student')
            db.session.add(role)
            db.session.commit()

        ay = AcademicYear.query.filter_by(year_label='2025-2026').first()
        if not ay:
            ay = AcademicYear(year_label='2025-2026', is_current=True, start_date=date(2025, 6, 1), end_date=date(2026, 4, 30))
            db.session.add(ay)
            db.session.commit()

        c = ClassModel.query.filter_by(code='CLS-TEST-10').first()
        if not c:
            c = ClassModel(name='Class 10', code='CLS-TEST-10', category='High School')
            db.session.add(c)
            db.session.commit()

        sec = Section.query.filter_by(class_id=c.id, name='Section A').first()
        if not sec:
            sec = Section(class_id=c.id, name='Section A')
            db.session.add(sec)
            db.session.commit()

        u = User.query.filter_by(username='test_student_unique').first()
        if not u:
            u = User(username='test_student_unique', email='student_unique@test.com', role='Student')
            u.set_password('pass123')
            db.session.add(u)
            db.session.commit()

        self.student = Student.query.filter_by(admission_number='ADM-TEST-101').first()
        if not self.student:
            self.student = Student(
                user_id=u.id,
                admission_number='ADM-TEST-101',
                roll_number='1001',
                first_name='John',
                last_name='Doe',
                gender='Male',
                date_of_birth=date(2010, 1, 1),
                class_id=c.id,
                section_id=sec.id,
                academic_year_id=ay.id
            )
            db.session.add(self.student)
            db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_student_creation(self):
        st = Student.query.filter_by(admission_number='ADM-TEST-101').first()
        self.assertIsNotNone(st)
        self.assertEqual(st.full_name, 'John Doe')
        self.assertEqual(st.class_obj.name, 'Class 10')

    def test_grade_calculation(self):
        subj = Subject(name='Mathematics', code='MATH-TEST-10', class_id=1, pass_marks=40, max_marks=100)
        db.session.add(subj)
        db.session.commit()

        m = Mark(examination_id=1, student_id=self.student.id, subject_id=subj.id, internal_marks=20, theory_marks=70, practical_marks=0, total_marks=90)
        m.calculate_grade(max_marks=100, pass_marks=40)

        self.assertEqual(m.total_marks, 90.0)
        self.assertEqual(m.grade, 'A+')
        self.assertTrue(m.is_pass)


if __name__ == '__main__':
    unittest.main()
