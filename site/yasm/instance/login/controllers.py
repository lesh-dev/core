"""
.. _login_controllers:

Url dispatching file of :ref:`login <login>` module

|contains|
 * module - `Blueprint <http://exploreflask.com/en/latest/blueprints.html>`_ which provides urls and logic
 * lm - `flask_login.LoginManager <https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager>`_

|depends|
 * :ref:`oauth <oauth>` module
 * :ref:`database <database>`
 * :ref:`login forms <login_forms>`

|used|
 * :ref:`login <login>` module
"""
from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import login_user, logout_user
from ..menu import menu
from werkzeug.security import check_password_hash

from instance.login.oauth2 import OAuthSignIn
from instance.login.forms import LoginForm

from instance.generated.models.stub import lm, db
from instance.generated.api import decorators
from instance.generated.models.yasm.database import Person, DirectLogin


module = Blueprint('login', __name__, url_prefix='/login')

lm.unauthorized_handler(lambda *args, **kwargs: redirect(url_for('login.index')))


def user_login(login, password):
    logins = (DirectLogin
              .query
              .filter(DirectLogin.login == login)
              .filter(DirectLogin.type == 'pbkdf2')
              .all())
    if len(logins) != 1:
        return False
    user = logins[0]
    if check_password_hash('pbkdf2:{}'.format(user.password_hash), password):
        user = user.person
        login_user(user)
        return True
    return False


@module.route('/', methods=['GET', 'POST'])
def index():
    if LoginForm().validate_on_submit():
        if user_login(request.form['login'], request.form['password']):
            return redirect('i')
    form = LoginForm(request.form)
    return render_template(
        "login/base.html",
        menu=menu,
        form=form
    )


@module.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@module.route('/callback/<provider>')
@decorators.personalize
def oauth_callback(provider, current_user):
    oauth = OAuthSignIn.get_provider(provider)
    user_info = oauth.callback()
    provider_type, user_id = user_info[0], user_info[1]
    if not current_user.is_anonymous:
        return redirect(url_for('internal.index'))
    if user_id is None:
        flash('Authentication failed.')
        return redirect('/login/')
    user = (Person
            .query
            .join(DirectLogin)
            .filter(DirectLogin.type == provider_type)
            .filter(DirectLogin.password_hash == str(user_id))
            .first())
    if not user:
        return redirect(url_for('login.error'))
    login_user(user, True)
    return redirect(url_for('internal.index'))


@module.route('/logout')
@decorators.personalize
def logout(current_user):
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login.index'))


@module.route('/error')
def error():
    return """<h1>No user found with these credentials, ask your curator about this situation and try later</h1>
    <br>
    <a href='/login'>login</a>""", 401
