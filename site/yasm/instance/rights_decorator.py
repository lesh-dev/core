from flask_login import current_user
from functools import wraps


def has_rights(right):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if current_user.rights is not None and current_user.is_authenticated and right in current_user.rights:
                return f(*args, **kwargs)
            else:
                return "<h1>You have no power here!</h1>", 403
        return decorated
    return decorator
