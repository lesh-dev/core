from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('test', __name__, url_prefix='/test')

from .api_course import module as api_course_module
module.register_blueprint(api_course_module)
