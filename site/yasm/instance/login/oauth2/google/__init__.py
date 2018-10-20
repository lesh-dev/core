from ..base import OAuthSignIn
import google_auth_oauthlib.flow
from flask import redirect, request, json
import googleapiclient.discovery
import os

class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.service = google_auth_oauthlib.flow.Flow.from_client_config(
            self.config,
            scopes=[
                'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/plus.me',
                'https://www.googleapis.com/auth/userinfo.profile'
            ])
        self.service.redirect_uri = self.get_callback_url()
        self.authorization_url, self.state = self.service.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

    def authorize(self):
        return redirect(self.authorization_url)

    def callback(self):
        def decode_json(payload):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None

        if os.environ.get('OAUTHLIB_INSECURE_TRANSPORT'):
            self.service.oauth2session._state = request.args['state']
        self.service.fetch_token(authorization_response=request.url)
        auth = googleapiclient.discovery.build('oauth2', 'v2', credentials=self.service.credentials)
        me = auth.userinfo().get().execute()
        return (
            'google',
            me['id'],
            me
        )