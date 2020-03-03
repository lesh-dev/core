from ....NestableBlueprint import NestableBlueprint

module = NestableBlueprint('person', __name__, url_prefix='/person')

from .api_personal import module as api_personal_module
module.register_blueprint(api_personal_module)
from .api_people import module as api_people_module
module.register_blueprint(api_people_module)
