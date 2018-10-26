from flask_login import current_user
from functools import wraps


def has_rights(right):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.is_authenticated and right in current_user.rights:
                return f(*args, **kwargs)
        return decorated
    return decorator