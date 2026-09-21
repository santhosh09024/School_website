import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_upload_file(file_obj, subfolder=''):
    """
    Saves an uploaded file to static/uploads/<subfolder> with a safe unique name.
    """
    if not file_obj or file_obj.filename == '':
        return None

    if allowed_file(file_obj.filename):
        ext = file_obj.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(target_dir, exist_ok=True)
        
        file_path = os.path.join(target_dir, filename)
        file_obj.save(file_path)
        
        # Return relative URL path for DB storage
        if subfolder:
            return f"uploads/{subfolder}/{filename}"
        return f"uploads/{filename}"
    return None


def generate_application_number():
    """Generates unique admission application number like ADM-2026-98765"""
    return f"ADM-2026-{uuid.uuid4().hex[:6].upper()}"


def generate_receipt_number():
    """Generates unique fee receipt number like REC-2026-12345"""
    return f"REC-2026-{uuid.uuid4().hex[:6].upper()}"


def get_school_settings():
    """Returns a dict of all school settings from database or sensible defaults"""
    from app.models.cms import SchoolSetting
    defaults = {
        'school_name': 'EduLead INTERNATIONAL SCHOOL',
        'tagline': 'Nurturing Minds, Shaping Futures',
        'address': '123 Knowledge Parkway, Education City',
        'phone': '+91 98765 43210',
        'email': 'info@eduleadschool.com',
        'office_hours': 'Mon - Sat: 8:00 AM - 4:00 PM',
        'principal_name': 'Dr. Eleanor Vance, Ph.D.',
        'chairman_name': 'Prof. Arthur Pendelton',
        'academic_year': '2025-2026',
        'footer_text': '© 2026 EduLead International School. All Rights Reserved.'
    }
    try:
        settings = SchoolSetting.query.all()
        for setting in settings:
            defaults[setting.key] = setting.value
    except Exception:
        pass
    return defaults
