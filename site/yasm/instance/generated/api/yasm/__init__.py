from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('yasm', __name__, url_prefix='/yasm')

from .internal import module as internal_module
module.register_blueprint(internal_module)
