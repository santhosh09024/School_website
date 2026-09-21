import os
from flask import Flask, render_template
from config import config
from app.extensions import db, login_manager, csrf
from app.utils.helpers import get_school_settings


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Ensure upload & instance directories exist
    os.makedirs(os.path.join(app.root_path, '..', 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'photos'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'documents'), exist_ok=True)

    # Inject global variables into Jinja context
    @app.context_processor
    def inject_globals():
        return {
            'school_settings': get_school_settings()
        }

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.student import student_bp
    from app.routes.teacher import teacher_bp
    from app.routes.academic import academic_bp
    from app.routes.attendance import attendance_bp
    from app.routes.examination import exam_bp
    from app.routes.fee import fee_bp
    from app.routes.cms_admin import cms_bp
    from app.routes.reports import reports_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(student_bp, url_prefix='/admin/students')
    app.register_blueprint(teacher_bp, url_prefix='/admin/teachers')
    app.register_blueprint(academic_bp, url_prefix='/admin/academic')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(exam_bp, url_prefix='/examinations')
    app.register_blueprint(fee_bp, url_prefix='/fees')
    app.register_blueprint(cms_bp, url_prefix='/admin/cms')
    app.register_blueprint(reports_bp, url_prefix='/admin/reports')
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Register Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    # Auto-initialize database & seed data in development
    with app.app_context():
        db.create_all()
        from app.utils.seed_data import seed_database
        try:
            seed_database()
        except Exception as ex:
            print(f"Database seed note: {ex}")

    return app
