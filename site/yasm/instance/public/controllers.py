from flask import Blueprint, render_template
from flask_login import current_user
from ..menu import menu

module = Blueprint('public', __name__, url_prefix='')


@module.route('/', methods=['GET'])
def index():
    return render_template(
        "public/base.html",
        menu=menu,
        person=current_user,
    )
