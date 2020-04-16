from flask_login import current_user


def personalize(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, current_user=current_user)
    wrapper.__name__ = func.__name__
    return wrapper


