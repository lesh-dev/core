from flask import send_file, redirect, url_for
from flask_login import login_required
from ..rights_decorator import has_rights
from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('docs', __name__, url_prefix='/docs')


@module.route('/', methods=['GET'])
@login_required
@has_rights('docs')
def _index():
    return redirect('/docs/html/index.html')


@module.route('/<path:path>', methods=['GET'])
@login_required
@has_rights('docs')
def index(path):
    return send_file(
        "templates/docs/" + path
    )
