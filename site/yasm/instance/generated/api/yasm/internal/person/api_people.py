from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APIPeople', __name__, url_prefix='/APIPeople')

module.add_decorator(login_required)


@module.route('FetchPerson', methods=['POST'])
def _fetch_person(
):
    req = models.yasm.internal.person.FetchPersonRequest.from_json(request.json)
    return Interface.fetch_person(
        req,
    ).to_string()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.fetch_person = obj.fetch_person
        return obj

    @staticmethod
    def fetch_person(
        request,
):
        raise NotImplementedError

