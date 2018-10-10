from flask import Blueprint, url_for, redirect, flash
from flask_login import current_user, login_user, logout_user
from .oauth2 import OAuthSignIn
from ..database import Person, Contact, db

module = Blueprint('login', __name__, url_prefix='/login')


@module.route('/')
def root():
    return "<ul>" \
           "<li>" \
           "<a href='/login/authorize/facebook'>facebook</a>" \
           "</li>" \
           "<li>" \
           "<a href='/login/authorize/vk'>vk</a>" \
           "</li>" \
           "</ul>"


@module.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect('/admin')
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@module.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    type, id, username = oauth.callback()
    if id is None:
        flash('Authentication failed.')
        return redirect('/')
    user = Person.query.join(Contact).filter(Contact.name == type).filter(Contact.value == id).first()
    if not user:
        return redirect('/')
    login_user(user, True)
    return redirect(url_for('admin.index'))


@module.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect('/login')