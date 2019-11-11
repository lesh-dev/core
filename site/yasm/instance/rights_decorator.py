from flask_login import current_user
from flask import url_for, redirect
from functools import wraps
from instance.login import lm


def has_rights_check(right):
    if current_user.is_authenticated:
        if right is None:
            return None
        if current_user.rights is None or right not in current_user.rights:
            return "<h1>You have no power here!</h1>", 403
    else:
        return lm.unauthorized_callback()


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
