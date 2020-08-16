from instance.generated.api.yasm.internal.person.api_people import Interface
from instance.generated.models.yasm.database import Person


class APIPeople(Interface):
    @staticmethod
    def fetch_person(
        request,
    ):
        person = Person.query.get(int(request.id))
        person.avas = sorted(person.avas, key=lambda ava: ava.timestamp)[-6:]
        return person
