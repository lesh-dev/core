from flask_login import current_user
from functools import wraps


def has_rights_check(right):
    if current_user.is_authenticated and not (current_user.rights is not None and current_user.is_authenticated and right in current_user.rights):
        return "<h1>You have no power here!</h1>", 403


def has_rights_check_function(right):
    return lambda: has_rights_check(right)


def has_rights(right):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            resp = has_rights_check(right)
            if resp is None:
                return f(*args, **kwargs)
            else:
                return resp
        return decorated
    return decorator
