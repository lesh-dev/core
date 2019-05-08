"""
.. _oauth:

Collection of oauth handlers

|depends|
 * :ref:`base <oauth_base>` oauth
 * :ref:`facebook <oauth_facebook>` oauth
 * :ref:`vk <oauth_vk>` oauth
 * :ref:`yandex <oauth_yandex>` oauth
 * :ref:`google <oauth_google>` oauth

|used|
 * :ref:`login controllers <login_controllers>` module
"""

from .facebook import FacebookSignIn
from .vk import VkSignIn
from .base import OAuthSignIn
from .yandex import YandexSignIn
from .google import GoogleSignIn
