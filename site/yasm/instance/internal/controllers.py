from instance.generated.api.NestableBlueprint import NestableBlueprint
from instance.rights_decorator import has_rights_check_function
from instance.menu import menu
from flask import render_template


module = NestableBlueprint('internal', __name__, url_prefix='/i')

module.before_request(has_rights_check_function(None))

@module.route('/', methods=['GET'])
@module.route('/<path:path>', methods=['GET'])
def index(path=""):
    return render_template(
        "internal/base.html",
        menu=menu,
    )
