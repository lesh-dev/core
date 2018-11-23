from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..menu import menu

module = Blueprint('react-components', __name__, url_prefix='/RC')


@module.route('/', methods=['GET'])
@module.route('/<path:path>', methods=['GET'])
# @login_required
def index(path="dummy"):
    return render_template(
        "react-components/base.html",
        menu=menu,
        person=current_user,
    )
