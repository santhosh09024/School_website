from datetime import datetime
from app.extensions import db


class Examination(db.Model):
    __tablename__ = 'examinations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Mid-Term Exam, Annual Examination, Unit Test 1
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    class_obj = db.relationship('ClassModel', backref='examinations')
    exam_subjects = db.relationship('ExamSubject', backref='examination_obj', lazy='dynamic', cascade='all, delete-orphan')
    marks = db.relationship('Mark', backref='examination_obj', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Examination {self.title}>'


class ExamSubject(db.Model):
    __tablename__ = 'exam_subjects'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    max_marks = db.Column(db.Float, default=100.0)
    pass_marks = db.Column(db.Float, default=40.0)
    exam_date = db.Column(db.Date)

    def __repr__(self):
        return f'<ExamSubject Exam:{self.examination_id} Subject:{self.subject_id}>'


class Mark(db.Model):
    __tablename__ = 'marks'

    id = db.Column(db.Integer, primary_key=True)
    examination_id = db.Column(db.Integer, db.ForeignKey('examinations.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    internal_marks = db.Column(db.Float, default=0.0)
    theory_marks = db.Column(db.Float, default=0.0)
    practical_marks = db.Column(db.Float, default=0.0)
    total_marks = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, default=0.0)
    grade = db.Column(db.String(10), default='F')  # A+, A, B, C, D, F
    is_pass = db.Column(db.Boolean, default=True)
    remarks = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('examination_id', 'student_id', 'subject_id', name='unique_exam_student_subject_mark'),
    )

    def calculate_grade(self, max_marks=100.0, pass_marks=40.0):
        self.total_marks = round(self.internal_marks + self.theory_marks + self.practical_marks, 2)
        if max_marks > 0:
            self.percentage = round((self.total_marks / max_marks) * 100, 2)
        else:
            self.percentage = 0.0

        self.is_pass = self.total_marks >= pass_marks

        if not self.is_pass:
            self.grade = 'F'
        elif self.percentage >= 90:
            self.grade = 'A+'
        elif self.percentage >= 80:
            self.grade = 'A'
        elif self.percentage >= 70:
            self.grade = 'B'
        elif self.percentage >= 60:
            self.grade = 'C'
        elif self.percentage >= 50:
            self.grade = 'D'
        else:
            self.grade = 'E'

    def __repr__(self):
        return f'<Mark Student:{self.student_id} Subject:{self.subject_id} Total:{self.total_marks}>'
