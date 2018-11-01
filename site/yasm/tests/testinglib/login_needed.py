from flask_login import login_user
import instance


def login_needed(id):
    def decorator(func):
        def decorated(*args, **kwargs):
            login_user(user=instance.login.controllers.load_user(id))
            func(*args, **kwargs)
        return decorated
    return decorator
