from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

@module.route('', methods=['POST'])
def _():
    Interface.()


@module.route('', methods=['POST'])
def _():
    Interface.()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface. = obj.
        Interface. = obj.
        return obj

    @staticmethod
    def (request):
        raise NotImplementedError

    @staticmethod
    def (request):
        raise NotImplementedError

