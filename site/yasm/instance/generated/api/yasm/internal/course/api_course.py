from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

module.add_decorator(login_required)


@module.route('FetchCourse', methods=['POST'])
def _fetch_course(
):
    req = models.yasm.internal.course.FetchCourseRequest.from_json(request.json)
    return Interface.fetch_course(
        req,
    ).to_string()


@module.route('PatchTeachers', methods=['POST'])
def _patch_teachers(
):
    req = models.yasm.internal.course.PatchTeachersRequest.from_json(request.json)
    return Interface.patch_teachers(
        req,
    ).to_string()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.fetch_course = obj.fetch_course
        Interface.patch_teachers = obj.patch_teachers
        return obj

    @staticmethod
    def fetch_course(
        request,
    ):
        raise NotImplementedError

    @staticmethod
    def patch_teachers(
        request,
    ):
        raise NotImplementedError

