from datetime import datetime
from app.extensions import db


class FeeCategory(db.Model):
    __tablename__ = 'fee_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Tuition Fee, Admission Fee, Transport, Exam Fee, etc.
    description = db.Column(db.String(255))
    default_amount = db.Column(db.Float, default=0.0)

    fee_structures = db.relationship('FeeStructure', backref='category_obj', lazy='dynamic')

    def __repr__(self):
        return f'<FeeCategory {self.name}>'


class FeeStructure(db.Model):
    __tablename__ = 'fee_structures'

    id = db.Column(db.Integer, primary_key=True)
    academic_year_id = db.Column(db.Integer, db.ForeignKey('academic_years.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    fee_category_id = db.Column(db.Integer, db.ForeignKey('fee_categories.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payments = db.relationship('FeePayment', backref='structure_obj', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<FeeStructure Class:{self.class_id} Amount:{self.amount}>'


class FeePayment(db.Model):
    __tablename__ = 'fee_payments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    fee_structure_id = db.Column(db.Integer, db.ForeignKey('fee_structures.id'), nullable=False)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False)
    transaction_id = db.Column(db.String(100))
    amount_paid = db.Column(db.Float, nullable=False)
    pending_amount = db.Column(db.Float, default=0.0)
    payment_mode = db.Column(db.String(50), default='Cash')  # Cash, Online, Cheque, Bank Transfer
    payment_date = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(30), default='Paid')  # Paid, Partial, Pending
    remarks = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FeePayment Receipt:{self.receipt_number} Amount:{self.amount_paid}>'
