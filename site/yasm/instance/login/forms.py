"""
.. _login_forms:

Login forms declaration file

|used|
 * :ref:`login controllers <login_controllers>`
"""
import wtforms
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    login = wtforms.StringField('login', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('password', validators=[wtforms.validators.DataRequired()])
