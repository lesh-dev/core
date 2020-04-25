from instance.generated.api.yasm.internal.person.api_people import Interface
from instance.generated.models.yasm.database import Person
from instance.generated.enums.yasm.database import DatabaseStatus


class APIPeople(Interface):
    @staticmethod
    def fetch_person(
        request,
    ):
        person = Person.query.get(int(request.id))
        person.avas = [ava for ava in person.avas if ava.status == DatabaseStatus.relevant]
        return person
