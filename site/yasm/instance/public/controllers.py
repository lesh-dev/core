from flask import Blueprint, render_template
from flask_login import current_user

from instance.generated.models.yasm.database import Department, Person
from instance.generated.models.stub import db
from instance.menu import menu
from instance.public.forms import RegisterForm

module = Blueprint('public', __name__, url_prefix='')


@module.route('/', methods=['GET'])
def index():
    return render_template(
        "public/base.html",
        menu=menu,
        person=current_user,
    )


@module.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        math_dep = Department.query.filter(Department.department_title == 'Математическое').one_or_none()
        new_person = Person()
        new_person.first_name = form.first_name.data
        new_person.last_name = form.last_name.data
        new_person.patronymic = form.patronymic.data
        new_person.email = form.email.data
        new_person.cellular = form.phone.data
        new_person.other_contacts = form.other.data
        new_person.school = form.school.data
        new_person.ank_class = form.grade.data
        new_person.achievements = form.olympiads.data
        new_person.hobby = form.info.data
        new_person.lesh_ref = form.referer.data
        new_person.department = math_dep
        db.session.add(new_person)
        db.session.commit()
        return "DONE!"
    return render_template(
        "public/register-form.html",
        menu=menu,
        form=form,
    )
