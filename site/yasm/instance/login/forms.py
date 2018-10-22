import wtforms


class LoginForm(wtforms.Form):
    login = wtforms.StringField('Login:')
    password = wtforms.PasswordField('Password:')