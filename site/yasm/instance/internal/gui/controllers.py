from flask import render_template
from flask_login import login_required, current_user
from instance.menu import menu
from instance.admin.side import side
from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('internal-gui', __name__, url_prefix='')


@module.route('/', methods=['GET'])
@module.route('/<path:path>', methods=['GET'])
def index(path=""):
    return render_template(
        "internal/base.html",
        menu=menu,
    )
