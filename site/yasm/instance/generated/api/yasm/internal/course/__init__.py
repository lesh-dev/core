from ....NestableBlueprint import NestableBlueprint

module = NestableBlueprint('course', __name__, url_prefix='/course')

from .api_course import module as api_course_module
module.register_blueprint(api_course_module)
