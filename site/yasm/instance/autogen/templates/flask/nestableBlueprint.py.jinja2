from functools import reduce
from flask import Blueprint


class NestableBlueprint(Blueprint):

    def __init__(self, *args, **kwargs):
        super(NestableBlueprint, self).__init__(*args, **kwargs)
        self.before_request_functions = []
        self.after_request_functions = []
        self.decorators = []

    def add_decorator(self, deco):
        self.decorators.append(deco)

    def route(self, rule, **options):
        def decorator(f):
            wrap = super(NestableBlueprint, self).route(rule, **options)
            f = reduce(lambda f, deco: deco(f), self.decorators, f)
            return wrap(f)
        return decorator


    def register_blueprint(self, blueprint, **options):
        for function in self.before_request_functions:
            blueprint.before_request(function)
        for function in self.after_request_functions:
            blueprint.after_request(function)

        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            name = (state.blueprint.name or u"") + '.' + (options.get('name', blueprint.name) or u"")
            if 'name' in options:
                del options['name']

            blueprint.name = name

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)

    def before_request(self, f):
        super(NestableBlueprint, self).before_request(f)
        self.before_request_functions.append(f)

    def after_request(self, f):
        super(NestableBlueprint, self).after_request(f)
        self.after_request_functions.append(f)