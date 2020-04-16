from ..NestableBlueprint import NestableBlueprint

module = NestableBlueprint('builtin', __name__, url_prefix='/builtin')

from .api_builtin import module as api_builtin_module
module.register_blueprint(api_builtin_module)
