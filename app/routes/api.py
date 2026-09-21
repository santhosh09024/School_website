from flask import Blueprint, jsonify, request
from app.models import Student, Teacher, Attendance, Notice, Event, Mark, Examination, ClassModel, ContactMessage

api_bp = Blueprint('api', __name__)


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'status': 'success',
        'data': {
            'total_students': Student.query.count(),
            'total_teachers': Teacher.query.count(),
            'total_classes': ClassModel.query.count(),
            'total_notices': Notice.query.filter_by(is_published=True).count(),
            'unread_messages': ContactMessage.query.filter_by(is_read=False).count()
        }
    })


@api_bp.route('/students', methods=['GET'])
def get_students():
    class_id = request.args.get('class_id', type=int)
    query = Student.query
    if class_id:
        query = query.filter_by(class_id=class_id)

    students = query.all()
    results = [{
        'id': s.id,
        'admission_number': s.admission_number,
        'roll_number': s.roll_number,
        'name': s.full_name,
        'class': s.class_obj.name if s.class_obj else '',
        'gender': s.gender
    } for s in students]

    return jsonify({'status': 'success', 'count': len(results), 'data': results})


@api_bp.route('/notices', methods=['GET'])
def get_notices():
    notices = Notice.query.filter_by(is_published=True).order_by(Notice.created_at.desc()).limit(10).all()
    results = [{
        'id': n.id,
        'title': n.title,
        'content': n.content,
        'publish_date': n.publish_date.isoformat() if n.publish_date else '',
        'attachment': n.attachment_path
    } for n in notices]

    return jsonify({'status': 'success', 'data': results})


@api_bp.route('/events', methods=['GET'])
def get_events():
    events = Event.query.filter_by(is_upcoming=True).order_by(Event.event_date.asc()).all()
    results = [{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'date': e.event_date.isoformat(),
        'time': e.event_time,
        'location': e.location
    } for e in events]

    return jsonify({'status': 'success', 'data': results})


@api_bp.route('/results/<identifier>', methods=['GET'])
def check_result(identifier):
    student = Student.query.filter(
        (Student.admission_number == identifier) |
        (Student.roll_number == identifier)
    ).first()

    if not student:
        return jsonify({'status': 'error', 'message': 'Student not found'}), 404

    latest_exam = Examination.query.filter_by(class_id=student.class_id, is_published=True).order_by(Examination.start_date.desc()).first()
    if not latest_exam:
        return jsonify({'status': 'error', 'message': 'No published examination results available'}), 404

    marks = Mark.query.filter_by(examination_id=latest_exam.id, student_id=student.id).all()
    marks_list = [{
        'subject': m.subject_obj.name if m.subject_obj else '',
        'internal': m.internal_marks,
        'theory': m.theory_marks,
        'practical': m.practical_marks,
        'total': m.total_marks,
        'percentage': m.percentage,
        'grade': m.grade,
        'pass': m.is_pass
    } for m in marks]

    return jsonify({
        'status': 'success',
        'student': {
            'name': student.full_name,
            'admission_number': student.admission_number,
            'roll_number': student.roll_number,
            'class': student.class_obj.name if student.class_obj else ''
        },
        'exam': latest_exam.title,
        'marks': marks_list
    })
