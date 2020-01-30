from instance.NestableBlueprint import NestableBlueprint

module = NestableBlueprint('APICourse', __name__, url_prefix='/APICourse')

@module.route('PatchTeachers', methods=['POST'])
def _patch_teachers():
    Interface.patch_teachers()


@module.route('TMP', methods=['POST'])
def _tmp():
    Interface.tmp()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.patch_teachers = obj.patch_teachers
        Interface.tmp = obj.tmp
        return obj

    @staticmethod
    def patch_teachers(request):
        raise NotImplementedError

    @staticmethod
    def tmp(request):
        raise NotImplementedError

