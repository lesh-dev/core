from ..base import OAuthSignIn
from rauth import OAuth2Service
from flask import redirect, request, json


class VkSignIn(OAuthSignIn):
    def __init__(self):
        super(VkSignIn, self).__init__('vk')
        self.service = OAuth2Service(
            name='vk',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://api.vk.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            v='5.85',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
            answer = json.loads(payload.decode('utf-8'))
            self.user_id = answer['user_id']
            return answer

        if 'code' not in request.args:
            return None, None, None
        self.service.get_auth_session(
            data={'code': request.args['code'],
                  'client_secret': self.consumer_secret,
                  'client_id': self.consumer_id,
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        return (
            'vk',
            self.user_id,
            None
        )
