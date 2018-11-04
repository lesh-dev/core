def request_needed(engine):
    def decorator(func):
        def decorated(*args, **kwargs):
            with engine.test_request_context():
                func(*args, **kwargs)
        return decorated
    return decorator
