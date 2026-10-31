import os
import sys
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
    port = int(os.getenv('PORT', 5000))

    if sys.platform == 'win32':
        # Windows: use waitress (gunicorn doesn't support Windows)
        from waitress import serve
        print(f" * Running on http://0.0.0.0:{port} (waitress)")
        serve(app, host='0.0.0.0', port=port)
    else:
        # Linux/Mac: use Flask dev server (gunicorn used via Procfile in production)
        app.run(host='0.0.0.0', port=port, debug=True)
