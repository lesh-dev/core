from flask import Blueprint, render_template
from ..menu import menu

module = Blueprint('react-components', __name__, url_prefix='/RC')

@module.route('/', methods=['GET'])
@module.route('/<path:path>', methods=['GET'])
def index(path="dummy"):
    return render_template(
        "react-components/base.html",
        menu=menu
    )
