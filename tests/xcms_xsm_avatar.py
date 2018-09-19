#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

import xsm
import xtest_common
import requests


class XcmsXsmAvatar(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks person user functional and VK's avatar display feature
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * check person's avatar.
    * change avatar to xyz100
    * check person's avatar.
    * change avatar to idNNN
    * check person's avatar.
    * change avatar to default
    * check person's avatar (stalin50).
    * change avatar to non-existing VK page
    * check person's avatar
    """

    def check_avatar(self, person, default):
        avatar_src = self.getImageSrcById("avatar")
        logging.debug("Avatar source: %s", avatar_src)
        fail_condition = ("stalin50" in avatar_src) ^ default
        response = requests.head(avatar_src, verify=False).status_code
        if fail_condition:
            self.failTest("Wrong avatar detected, expected {} image. VK ID: {}".format(
                "default" if default else "custom",
                person.social_profile,
            ))
        elif response != 200 and response != 501:
            # vk says HTTP 501 on deactivated profiles
            self.failTest("Wrong response, expected '200' got {}. request: {}, VK ID  {}".format(
                response,
                avatar_src,
                person.social_profile,
            ))

    def run(self):
        self.ensure_logged_off()
        self.perform_login_as_manager()
        self.goto_xsm()
        self.goto_xsm_all_people()
        self.goto_xsm_add_person()

        person = xsm.Person(self)
        person.input(
            last_name=u"Аватаров",
            first_name=u"Пётр",
            patronymic=u"Палыч",
            social_profile="https://vk.com/vdm_p",
            random=True,
        )
        person.back_to_person_view()
        self.check_avatar(person, default=False)

        # ok, now let's test xyz100 avatar.
        self.gotoEditPerson()
        person.input(social_profile="http://vk.com/vasya10")
        person.back_to_person_view()
        self.check_avatar(person, default=False)

        # ok, now let's test id123456 avatar.
        self.gotoEditPerson()
        person.input(social_profile="http://vk.com/id777314")
        person.back_to_person_view()
        self.check_avatar(person, default=False)

        # ok, now let's test default avatar.
        self.gotoEditPerson()
        person.input(social_profile="")
        person.back_to_person_view()
        self.check_avatar(person, default=True)

        # ok, now let's test non-existing VK page.
        self.gotoEditPerson()
        person.input(social_profile="http://vk.com/id12345678901234567890")
        person.back_to_person_view()
        self.check_avatar(person, default=True)
