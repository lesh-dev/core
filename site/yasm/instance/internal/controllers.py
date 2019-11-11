from instance.NestableBlueprint import NestableBlueprint
from instance.rights_decorator import has_rights_check_function

from instance.internal.api import api
from instance.internal.gui import gui


module = NestableBlueprint('internal', __name__, url_prefix='/i')

module.before_request(has_rights_check_function(None))

module.register_blueprint(gui)
module.register_blueprint(api)
