from instance.generated.api.yasm.internal.person.api_personal import Interface
from instance.generated.models.yasm.internal.person import GetProfileResponse, CoursesResponse, ContactList
from instance.generated.models.yasm.database import Person, Ava, Contact
from instance.generated.models.stub import db
from instance.generated.enums.yasm.database import DatabaseStatus
from instance.generated.enums.yasm.internal.person import ContactsPatchActions


class APIPersonal(Interface):
    @staticmethod
    def get_profile(
        request,
        current_user,
    ):
        ava = ''
        for avatar in current_user.avas:
            if avatar.status == DatabaseStatus.relevant.value:
                ava = avatar.ava
        return GetProfileResponse(
            id=current_user.id,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            nick_name=current_user.nick_name,
            ava=ava,
        )

    @staticmethod
    def get_profile_info(
        request,
        current_user,
    ):
        return fill_person(current_user)

    @staticmethod
    def get_courses(
        request,
        current_user,
    ):
        return CoursesResponse(
            courses=[ct.course for ct in current_user.courses],
        )

    @staticmethod
    def set_ava(
        request,
        current_user,
    ):
        for avatar in current_user.avas:
            avatar.status = DatabaseStatus.obsolete.value
        db.session.commit()
        ava = Ava(
            person=current_user,
            ava=request.new_ava,
            status=DatabaseStatus.relevant.value,
        )
        db.session.add(ava)
        db.session.commit()
        return ava

    @staticmethod
    def patch_contacts(
        request,
        current_user,
    ):
        contacts = {
            c.value: c
            for c in current_user.contacts
        }
        new_contacts = []
        for value, spec in request.patch.items():
            if value in contacts:
                if spec.action == ContactsPatchActions.add:
                    contacts[value].name = spec.name
                else:
                    db.session.delete(contacts[value])
            else:
                if spec.action == ContactsPatchActions.add:
                    new_contacts.append(
                        Contact(
                            person=current_user,
                            name=spec.name,
                            value=value,
                        )
                    )
        for contact in new_contacts:
            db.session.add(contact)
        db.session.commit()
        return ContactList(
            contacts=current_user.contacts,
        )

    @staticmethod
    def set_password(
        request,
        current_user,
    ):
        pass


def fill_person(person: Person):
    _ = person.person_schools
    _ = person.exams
    _ = person.courses
    _ = person.contacts
    return person
