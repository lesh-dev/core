"""
.. _login_controllers:

Url dispatching file of :ref:`login <login>` module

Contained variables
 * module - `Blueprint <http://exploreflask.com/en/latest/blueprints.html>`_ which provides urls and logic
 * lm - `flask_login.LoginManager <https://flask-login.readthedocs.io/en/latest/#flask_login.LoginManager>`_

Depends on
 * :ref:`oauth <oauth>` module
 * :ref:`database <database>`
 * :ref:`login forms <login_forms>`

Used in
 * :ref:`login <login>` module
"""
from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from .oauth2 import OAuthSignIn
from ..database import Person, Contact, DirectLogin, db
from ..menu import menu
from flask_login import LoginManager
from .forms import LoginForm
from werkzeug.security import check_password_hash

lm = LoginManager()

module = Blueprint('login', __name__, url_prefix='/login')

lm.unauthorized_handler(lambda *args, **kwargs: redirect(url_for('login.index')))


@lm.user_loader
def load_user(id):
    return Person.query.get(int(id))


def user_login(login, password):
    logins = (DirectLogin
              .query
              .filter(DirectLogin.login == login)
              .filter(DirectLogin.password_hash.startswith('pbkdf2:'))
              .all())
    if len(logins) != 1:
        return False
    user = logins[0]
    if check_password_hash(user.password_hash, password):
        user = user.person
        login_user(user)
        return True
    return False


@module.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if user_login(request.form['login'], request.form['password']):
            return redirect(url_for('personal.index'))
        else:
            pass
    form = LoginForm(request.form)
    return render_template(
        "login/base.html",
        menu=menu,
        person=current_user,
        form=form
    )


@module.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@module.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    user_info = oauth.callback()
    provider_type, user_id = user_info[0], user_info[1]
    if not current_user.is_anonymous:
        add_oauth(provider_type, user_id)
        return redirect(url_for('personal.index'))
    if user_id is None:
        flash('Authentication failed.')
        return redirect('/login/')
    user = (Person
            .query
            .join(DirectLogin)
            .filter(DirectLogin.password_hash == ('{provider_type}:{user_id}'
                                                  .format(provider_type=provider_type, user_id=user_id))
                    )
            .first())
    if not user:
        return redirect(url_for('login.error'))
    login_user(user, True)
    return redirect(url_for('personal.index'))


@module.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login.index'))


@module.route('/error')
def error():
    return """<h1>No user found with these credentials, ask your curator about this situation and try later</h1>
    <br>
    <a href='/login'>login</a>""", 401


def add_oauth(provider_type, user_id):
    dl = DirectLogin()
    dl.password_hash = '{provider_type}:{user_id}'.format(provider_type=provider_type, user_id=user_id)
    dl.person = current_user
    dl.login = 'OAUTH'
    db.session.add(dl)
    db.session.commit()
