from datetime import date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.extensions import db
from app.models import FeeCategory, FeeStructure, FeePayment, Student, ClassModel, AcademicYear
from app.utils.decorators import role_required
from app.utils.helpers import generate_receipt_number

fee_bp = Blueprint('fee', __name__)


@fee_bp.route('/')
@login_required
def index():
    categories = FeeCategory.query.all()
    structures = FeeStructure.query.all()
    classes = ClassModel.query.all()
    payments = FeePayment.query.order_by(FeePayment.payment_date.desc()).limit(50).all()

    return render_template(
        'dashboard/fees/index.html',
        categories=categories,
        structures=structures,
        classes=classes,
        payments=payments
    )


@fee_bp.route('/category/add', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def add_category():
    name = request.form.get('name')
    desc = request.form.get('description', '')
    amount = request.form.get('default_amount', type=float, default=0.0)

    if name:
        cat = FeeCategory(name=name, description=desc, default_amount=amount)
        db.session.add(cat)
        db.session.commit()
        flash(f'Fee category "{name}" created.', 'success')

    return redirect(url_for('fee.index'))


@fee_bp.route('/structure/add', methods=['POST'])
@login_required
@role_required('Super Admin', 'Admin')
def add_structure():
    class_id = request.form.get('class_id', type=int)
    fee_category_id = request.form.get('fee_category_id', type=int)
    amount = request.form.get('amount', type=float)
    due_date_str = request.form.get('due_date')

    ay = AcademicYear.query.filter_by(is_current=True).first()
    ay_id = ay.id if ay else 1

    if class_id and fee_category_id and amount:
        struct = FeeStructure(
            academic_year_id=ay_id,
            class_id=class_id,
            fee_category_id=fee_category_id,
            amount=amount,
            due_date=date.fromisoformat(due_date_str) if due_date_str else date.today()
        )
        db.session.add(struct)
        db.session.commit()
        flash('Fee structure created.', 'success')

    return redirect(url_for('fee.index'))


@fee_bp.route('/pay', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin', 'Admin')
def pay():
    if request.method == 'POST':
        student_id = request.form.get('student_id', type=int)
        fee_structure_id = request.form.get('fee_structure_id', type=int)
        amount_paid = request.form.get('amount_paid', type=float)
        mode = request.form.get('payment_mode', 'Cash')
        txn_id = request.form.get('transaction_id', '')
        remarks = request.form.get('remarks', '')

        struct = FeeStructure.query.get(fee_structure_id)
        pending = max(0.0, struct.amount - amount_paid) if struct else 0.0
        rec_no = generate_receipt_number()

        payment = FeePayment(
            student_id=student_id,
            fee_structure_id=fee_structure_id,
            receipt_number=rec_no,
            transaction_id=txn_id,
            amount_paid=amount_paid,
            pending_amount=pending,
            payment_mode=mode,
            status='Paid' if pending == 0 else 'Partial',
            remarks=remarks
        )
        db.session.add(payment)
        db.session.commit()

        flash(f'Payment recorded! Receipt No: {rec_no}', 'success')
        return redirect(url_for('fee.receipt', receipt_no=rec_no))

    students = Student.query.all()
    structures = FeeStructure.query.all()
    return render_template('dashboard/fees/pay.html', students=students, structures=structures)


@fee_bp.route('/receipt/<receipt_no>')
@login_required
def receipt(receipt_no):
    payment = FeePayment.query.filter_by(receipt_number=receipt_no).first_or_404()
    return render_template('dashboard/fees/receipt.html', payment=payment)
