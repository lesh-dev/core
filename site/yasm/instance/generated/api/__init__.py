from .NestableBlueprint import NestableBlueprint

module = NestableBlueprint('api', __name__, url_prefix='/api')

from .builtin import module as builtin_module
module.register_blueprint(builtin_module)
from .yasm import module as yasm_module
module.register_blueprint(yasm_module)
