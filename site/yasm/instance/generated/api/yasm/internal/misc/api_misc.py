from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APIMisc', __name__, url_prefix='/APIMisc')

module.add_decorator(login_required)


@module.route('Search', methods=['POST'])
def _search(
):
    req = models.yasm.internal.misc.SearchRequest.from_json(request.json)
    return Interface.search(
        req,
    ).to_string()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.search = obj.search
        return obj

    @staticmethod
    def search(
        request,
):
        raise NotImplementedError

