from flask_login import current_user


def personalize(func):
    def wrapper():
        return func(current_user=current_user)
    return wrapper


def ASD(func):
    raise NotImplementedError


def asd(func):
    raise NotImplementedError


