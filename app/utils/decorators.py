from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to restrict route access to specified roles.
    Example: @role_required('Admin', 'Super Admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash('Access denied: You do not have permission to view this resource.', 'danger')
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
