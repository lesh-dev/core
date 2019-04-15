"""
.. _oauth_base:

Base classes for oauth.

Used in
 * :ref:`oauth <oauth>` module
"""
from flask import url_for


class Auth(object):
    app = None

    @classmethod
    def init_app(cls, app):
        cls.app = app


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = Auth.app.config['OAUTH_CREDENTIALS'][provider_name]
        if self.provider_name == 'google':
            self.config = Auth.app.config['OAUTH_CREDENTIALS'][provider_name]
        else:
            self.consumer_id = credentials['id']
            self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('login.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]
