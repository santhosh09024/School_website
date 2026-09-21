from datetime import datetime
from app.extensions import db


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    students = db.relationship('Student', backref='parent_obj', lazy='dynamic')

    def __repr__(self):
        return f'<Parent {self.father_name} & {self.mother_name}>'


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    admission_number = db.Column(db.String(30), unique=True, nullable=False)
    roll_number = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    photo = db.Column(db.String(255), default='default_student.png')
    admission_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')  # Active, Graduated, Suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attendances = db.relationship('Attendance', backref='student_obj', lazy='dynamic', cascade='all, delete-orphan')
    marks = db.relationship('Mark', backref='student_obj', lazy='dynamic', cascade='all, delete-orphan')
    fee_payments = db.relationship('FeePayment', backref='student_obj', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f'<Student {self.full_name} ({self.admission_number})>'


class AdmissionApplication(db.Model):
    __tablename__ = 'admissions'

    id = db.Column(db.Integer, primary_key=True)
    application_number = db.Column(db.String(40), unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    class_applying = db.Column(db.String(50), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    previous_school = db.Column(db.String(150))
    previous_class = db.Column(db.String(50))
    academic_details = db.Column(db.Text)
    document_path = db.Column(db.String(255))
    student_photo = db.Column(db.String(255))
    status = db.Column(db.String(30), default='Pending')  # Pending, Under Review, Approved, Rejected
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdmissionApplication {self.application_number} - {self.student_name}>'
