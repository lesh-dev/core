from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    last_name = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    email = StringField('Электронная почта', validators=[DataRequired()])
    phone = IntegerField('Телефон', validators=[DataRequired()])
    other = TextAreaField('Другие контакты')
    school = StringField('Школа')
    grade = SelectField('Класс', choices=[
        (str(x), x) for x in [6, 7, 8, 9, 10, 11]
    ])
    olympiads = TextAreaField('Достижения на олимпиадах')
    info = TextAreaField('Расскажите немного о себе и ваших хобби', validators=[DataRequired()])
    referer = TextAreaField('Из какого источника вы узнали о нашей школе?')
    recaptcha = RecaptchaField()
