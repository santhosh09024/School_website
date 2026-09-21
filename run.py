import os
from app import create_app, db
from app.models import User, Role, Student, Teacher, Parent, ClassModel, Examination, Mark

app = create_app(os.getenv('FLASK_CONFIG') or 'development')


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Student': Student,
        'Teacher': Teacher,
        'Parent': Parent,
        'ClassModel': ClassModel,
        'Examination': Examination,
        'Mark': Mark
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
