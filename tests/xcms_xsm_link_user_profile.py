#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import user
import random_crap as rc


class XcmsXsmLinkUserProfile(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks XSM account - user link.
    It does following steps:
    * adds new user
    * adds XSM person with user-s email
    * check profile linking
    """

    def run(self):
        self.ensure_logged_off()

        inp_login = "xsm_link_" + rc.random_text(4)
        inp_name = u"XSM-Юзер-"
        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            name=inp_name,
            random=True,
            logout_admin=False,
            manager_rights=True,
        )

        self.closeAdminPanel()
        self.goto_xsm()
        self.goto_xsm_active()
        self.goto_xsm_add_person()
        person = xsm.Person(self)
        person.input(
            last_name=u"ИксЭсЭмов",
            first_name=u"Юзер",
            patronymic=u"Ламерович",
            email=u.email,
            random=True,
        )

        self.goto_root()
        self.performLogoutFromSite()

        if not self.perform_login(u.login, u.password):
            self.failTest("Cannot login as newly created user. ")

        self.gotoCabinet()
        self.assertBodyTextPresent("XSM")
        card_caption = u"Карточка участника в XSM"
        self.assertBodyTextPresent(card_caption)
        xsm_url_text = person.short_alias()
        self.gotoUrlByLinkText(xsm_url_text)
        self.assertBodyTextPresent(person.full_alias(), "We should get into our XSM person card. ")

        self.goto_root()
        self.performLogoutFromSite()

        self.perform_login_as_admin()
        self.gotoAdminPanel()
        self.gotoUserList()

        self.gotoUrlByPartialLinkText(inp_login, "Click on user name in the list")

        self.assertBodyTextPresent(card_caption, "We should see XSM card link. ")
        self.gotoUrlByLinkText(person.short_alias(), "Click on XSM card link")

        # TODO: here also should be link to user's XSM profile, if any.
