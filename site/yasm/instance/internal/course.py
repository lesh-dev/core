from instance.generated.api.yasm.internal.course.api_course import Interface
from instance.generated.models.yasm.database import Course


class APICourse(Interface):
    @staticmethod
    def fetch_course(
        request,
    ):
        return Course.query.get(int(request.id))