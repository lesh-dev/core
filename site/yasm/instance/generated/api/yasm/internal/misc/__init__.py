from ....NestableBlueprint import NestableBlueprint

module = NestableBlueprint('misc', __name__, url_prefix='/misc')

from .api_misc import module as api_misc_module
module.register_blueprint(api_misc_module)
