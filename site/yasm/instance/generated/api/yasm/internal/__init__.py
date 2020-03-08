from ...NestableBlueprint import NestableBlueprint

module = NestableBlueprint('internal', __name__, url_prefix='/internal')

from .course import module as course_module
module.register_blueprint(course_module)
from .person import module as person_module
module.register_blueprint(person_module)
from .misc import module as misc_module
module.register_blueprint(misc_module)
