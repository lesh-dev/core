"""
.. _login_forms:

Login forms declaration file

Contained variables

Depends on

Used in
 * :ref:`login controllers <login_controllers>`
"""
import wtforms


class LoginForm(wtforms.Form):
    login = wtforms.StringField('Login:')
    password = wtforms.PasswordField('Password:')
