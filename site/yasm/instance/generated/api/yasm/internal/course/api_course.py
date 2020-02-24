from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

module.before_request(login_required)
module.before_request(decorators.ASD)
module.before_request(decorators.personalize)


@module.route('PatchTeachers', methods=['POST'])
@decorators.asd
def _patch_teachers(
        current_user,
    ):
    req = models.yasm.internal.course.PatchTeachersRequest.from_json(request.json)
    return Interface.patch_teachers(
        req,
        current_user,
    ).serialize()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.patch_teachers = obj.patch_teachers
        return obj

    @staticmethod
    def patch_teachers(
        request,
        current_user,
    ):
        raise NotImplementedError

