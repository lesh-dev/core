from ...NestableBlueprint import NestableBlueprint

module = NestableBlueprint('internal', __name__, url_prefix='/internal')

from .course import module as course_module
module.register_blueprint(course_module)
