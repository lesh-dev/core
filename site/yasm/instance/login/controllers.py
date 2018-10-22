from flask import Blueprint, url_for, redirect, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from .oauth2 import OAuthSignIn
from ..database import Person, Contact, DirectLogin
from ..menu import menu
from flask_login import LoginManager
from .forms import LoginForm
from hashlib import md5

lm = LoginManager()


module = Blueprint('login', __name__, url_prefix='/login')


lm.unauthorized_handler(lambda *args, **kwargs: redirect(url_for('login.index')))


@lm.user_loader
def load_user(id):
    return Person.query.get(int(id))


def user_login(login, password):
    password_hash = md5(password.encode()).hexdigest()
    logins = DirectLogin.query.filter(DirectLogin.login == login).filter(DirectLogin.password_hash == password_hash).all()
    if len(logins) != 1:
        return False
    user = logins[0].person
    login_user(user)
    return True


@module.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if user_login(request.form['login'], request.form['password']):
            return redirect(url_for('admin.index'))
        else:
            pass
    form = LoginForm(request.form)
    return  render_template(
        "login/base.html",
        menu=menu,
        form=form
    )


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
    user_info = oauth.callback()
    type, id = user_info[0], user_info[1]
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