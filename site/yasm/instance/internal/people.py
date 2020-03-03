from instance.generated.api.yasm.internal.person.api_people import Interface
from instance.generated.models.yasm.database import Person


class APIPeople(Interface):
    @staticmethod
    def fetch_person(
        request,
    ):
        return Person.query.get(int(request.id))
