from instance.generated.api.yasm.internal.person.api_personal import Interface


class APIPersonal(Interface):
    @staticmethod
    def get_profile(
        request,
        current_user,
    ):
        pass

    @staticmethod
    def get_profile_info(
        request,
        current_user,
    ):
        pass

    @staticmethod
    def get_courses(
        request,
        current_user,
    ):
        pass

    @staticmethod
    def set_ava(
        request,
        current_user,
    ):
        pass

    @staticmethod
    def patch_contacts(
        request,
        current_user,
    ):
        pass

    @staticmethod
    def set_password(
        request,
        current_user,
    ):
        pass