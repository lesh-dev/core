from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('internal', __name__, url_prefix='/internal')

from .course import module as course_module
module.register_blueprint(course_module)
from .test import module as test_module
module.register_blueprint(test_module)
