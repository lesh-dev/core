from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

module.before_request(login_required)


@module.route('FetchCourse', methods=['POST'])
def _fetch_course(
    ):
    req = models.yasm.internal.course.FetchCourseRequest.from_json(request.json)
    return Interface.fetch_course(
        req,
    ).serialize()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.fetch_course = obj.fetch_course
        return obj

    @staticmethod
    def fetch_course(
        request,
    ):
        raise NotImplementedError

