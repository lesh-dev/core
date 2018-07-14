from flask import Blueprint, render_template
from ..menu import menu

module = Blueprint('public', __name__, url_prefix='/public')


@module.route('/', methods=['GET'])
def index():
    return render_template(
        "public/base.html",
        menu=menu
    )
