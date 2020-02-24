from flask import Blueprint


class NestableBlueprint(Blueprint):

    def __init__(self, *args, **kwargs):
        super(NestableBlueprint, self).__init__(*args, **kwargs)
        self.before_request_functions = []
        self.after_request_functions = []

    def register_blueprint(self, blueprint, **options):
        for function in self.before_request_functions:
            blueprint.before_request(function)
        for function in self.after_request_functions:
            blueprint.after_request(function)

        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)

    def before_request(self, f):
        super(NestableBlueprint, self).before_request(f)
        self.before_request_functions.append(f)


    def after_request(self, f):
        super(NestableBlueprint, self).after_request(f)
        self.after_request_functions.append(f)