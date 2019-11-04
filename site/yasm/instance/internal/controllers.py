from instance.NestableBlueprint import NestableBlueprint
from instance.internal.api import api
from instance.internal.gui import gui


module = NestableBlueprint('internal', __name__, url_prefix='/i')


module.register_blueprint(gui)
module.register_blueprint(api)
