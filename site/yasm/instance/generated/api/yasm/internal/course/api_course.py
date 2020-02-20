from flask import request
from instance.NestableBlueprint import NestableBlueprint
from ..... import models

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

@module.route('PatchTeachers', methods=['POST'])
def _patch_teachers():
    req = models.yasm.internal.course.PatchTeachersRequest.from_json(request.json)
    return Interface.patch_teachers(req).serialize()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.patch_teachers = obj.patch_teachers
        return obj

    @staticmethod
    def patch_teachers(request):
        raise NotImplementedError

