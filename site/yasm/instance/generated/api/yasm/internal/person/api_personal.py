from flask import request
from flask_login import login_required
from ....NestableBlueprint import NestableBlueprint
from .... import decorators
from ..... import models

module = NestableBlueprint('APIPersonal', __name__, url_prefix='/APIPersonal')

module.add_decorator(login_required)
module.add_decorator(decorators.personalize)


@module.route('GetProfile', methods=['POST'])
def _get_profile(
        current_user,
):
    req = models.google.protobuf.Empty.from_json(request.json)
    return Interface.get_profile(
        req,
        current_user,
    ).to_string()


@module.route('GetProfileInfo', methods=['POST'])
def _get_profile_info(
        current_user,
):
    req = models.google.protobuf.Empty.from_json(request.json)
    return Interface.get_profile_info(
        req,
        current_user,
    ).to_string()


@module.route('SetAva', methods=['POST'])
def _set_ava(
        current_user,
):
    req = models.yasm.internal.person.SetAvaRequest.from_json(request.json)
    return Interface.set_ava(
        req,
        current_user,
    ).to_string()


@module.route('PatchContacts', methods=['POST'])
def _patch_contacts(
        current_user,
):
    req = models.yasm.internal.person.ContactsPatch.from_json(request.json)
    return Interface.patch_contacts(
        req,
        current_user,
    ).to_string()


@module.route('SetPassword', methods=['POST'])
def _set_password(
        current_user,
):
    req = models.yasm.internal.person.SetPasswordRequest.from_json(request.json)
    return Interface.set_password(
        req,
        current_user,
    ).to_string()


@module.route('GetCourses', methods=['POST'])
def _get_courses(
        current_user,
):
    req = models.google.protobuf.Empty.from_json(request.json)
    return Interface.get_courses(
        req,
        current_user,
    ).to_string()


class Interface:
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        Interface.get_profile = obj.get_profile
        Interface.get_profile_info = obj.get_profile_info
        Interface.set_ava = obj.set_ava
        Interface.patch_contacts = obj.patch_contacts
        Interface.set_password = obj.set_password
        Interface.get_courses = obj.get_courses
        return obj

    @staticmethod
    def get_profile(
        request,
        current_user,
    ):
        raise NotImplementedError

    @staticmethod
    def get_profile_info(
        request,
        current_user,
    ):
        raise NotImplementedError

    @staticmethod
    def set_ava(
        request,
        current_user,
    ):
        raise NotImplementedError

    @staticmethod
    def patch_contacts(
        request,
        current_user,
    ):
        raise NotImplementedError

    @staticmethod
    def set_password(
        request,
        current_user,
    ):
        raise NotImplementedError

    @staticmethod
    def get_courses(
        request,
        current_user,
    ):
        raise NotImplementedError

