from functools import wraps
from flask import abort
from flask_login import current_user, login_required


def role_required(*roles):
    """Decorator that requires user to have one of the specified roles."""
    def decorator(f):
        @wraps(f)
        @login_required
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles and 'admin' not in roles:
                abort(403)
            # Admin always has access
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            # Check if user's role is in the allowed roles
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def staff_required(f):
    """Shortcut: requires staff or admin role."""
    return role_required('staff', 'admin')(f)


def admin_required(f):
    """Shortcut: requires admin role only."""
    return role_required('admin')(f)
