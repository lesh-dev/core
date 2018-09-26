from flask import Blueprint, url_for, redirect, flash
from flask_login import current_user, login_user
from .oauth2 import OAuthSignIn
from ..database import User, db

module = Blueprint('login', __name__, url_prefix='/login')

@module.route('/autorize/<provider>')
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
    social_id, username = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email="")
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('admin.index'))