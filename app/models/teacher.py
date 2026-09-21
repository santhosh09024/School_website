from datetime import datetime
from app.extensions import db


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_id = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(100), nullable=False)  # Senior Lecturer, Assistant Teacher, etc.
    department = db.Column(db.String(100), nullable=False)   # Science, Mathematics, English, etc.
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer, default=0)
    profile_photo = db.Column(db.String(255), default='default_teacher.png')
    bio = db.Column(db.Text)
    joining_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship('TeacherAssignment', backref='teacher_obj', lazy='dynamic', cascade='all, delete-orphan')
    timetables = db.relationship('Timetable', backref='teacher_obj', lazy='dynamic')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Teacher {self.full_name} ({self.employee_id})>'


class TeacherAssignment(db.Model):
    __tablename__ = 'teacher_assignments'

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    is_class_teacher = db.Column(db.Boolean, default=False)

    class_obj = db.relationship('ClassModel', backref='teacher_assignments')
    section_obj = db.relationship('Section', backref='teacher_assignments')
    subject_obj = db.relationship('Subject', backref='teacher_assignments')

    def __repr__(self):
        return f'<TeacherAssignment Teacher:{self.teacher_id} Class:{self.class_id}>'
