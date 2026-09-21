from datetime import datetime
from app.extensions import db


class AcademicYear(db.Model):
    __tablename__ = 'academic_years'

    id = db.Column(db.Integer, primary_key=True)
    year_label = db.Column(db.String(20), unique=True, nullable=False)  # e.g., "2025-2026"
    is_current = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship('Student', backref='academic_year', lazy='dynamic')
    examinations = db.relationship('Examination', backref='academic_year', lazy='dynamic')
    fee_structures = db.relationship('FeeStructure', backref='academic_year', lazy='dynamic')

    def __repr__(self):
        return f'<AcademicYear {self.year_label}>'


class ClassModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Class 10", "Grade 5"
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., "CLS-10"
    category = db.Column(db.String(50), default='Primary')  # Pre-primary, Primary, Middle, High, Higher Secondary
    description = db.Column(db.Text)

    sections = db.relationship('Section', backref='class_obj', lazy='dynamic', cascade='all, delete-orphan')
    subjects = db.relationship('Subject', backref='class_obj', lazy='dynamic', cascade='all, delete-orphan')
    students = db.relationship('Student', backref='class_obj', lazy='dynamic')
    fee_structures = db.relationship('FeeStructure', backref='class_obj', lazy='dynamic')
    timetables = db.relationship('Timetable', backref='class_obj', lazy='dynamic')

    def __repr__(self):
        return f'<ClassModel {self.name}>'


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)  # e.g., "Section A"
    capacity = db.Column(db.Integer, default=40)

    students = db.relationship('Student', backref='section_obj', lazy='dynamic')
    timetables = db.relationship('Timetable', backref='section_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Section {self.name} for Class ID {self.class_id}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    department = db.Column(db.String(100), default='General')
    pass_marks = db.Column(db.Float, default=40.0)
    max_marks = db.Column(db.Float, default=100.0)

    timetables = db.relationship('Timetable', backref='subject_obj', lazy='dynamic')
    marks = db.relationship('Mark', backref='subject_obj', lazy='dynamic')
    exam_subjects = db.relationship('ExamSubject', backref='subject_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Subject {self.name} ({self.code})>'


class Timetable(db.Model):
    __tablename__ = 'timetables'

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    day_of_week = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    period_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)  # e.g., "09:00 AM"
    end_time = db.Column(db.String(10), nullable=False)    # e.g., "09:45 AM"
    room_number = db.Column(db.String(20), default='101')

    def __repr__(self):
        return f'<Timetable Day:{self.day_of_week} Period:{self.period_number}>'
