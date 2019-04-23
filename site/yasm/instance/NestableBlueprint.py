"""
.. _nestable_blueprint:

Module, implementing nestable blueprints, provides us with better modularity

|used|
 * :ref:`admin <admin>` module
"""

from flask import Blueprint


class NestableBlueprint(Blueprint):
    """
    Nestable `Blueprint <http://exploreflask.com/en/latest/blueprints.html>`_
    taken from `Issue <https://github.com/pallets/flask/issues/593>`_
    """

    def register_blueprint(self, blueprint, **options):
        """
        see `flask documentation <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.register_blueprint>`_
        """
        def deferred(state):
            url_prefix = (state.url_prefix or u"") + (options.get('url_prefix', blueprint.url_prefix) or u"")
            if 'url_prefix' in options:
                del options['url_prefix']

            state.app.register_blueprint(blueprint, url_prefix=url_prefix, **options)

        self.record(deferred)
