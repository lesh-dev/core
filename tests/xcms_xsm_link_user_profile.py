#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmLinkUserProfile(xtest_common.XcmsTest):
    """
    This test checks XSM account - user link.
    It does following steps:
    * adds new user
    * adds XSM person with user-s email
    * check profile linking
    """

    def run(self):
        self.ensure_logged_off()
        inp_login = "xsm_link_" + random_crap.random_text(6)
        inp_email = random_crap.randomEmail()
        inp_pass = random_crap.random_text(8)
        inp_name = u"XSM-Юзер-" + random_crap.random_text(6)

        inp_login, inp_email, inp_pass, inp_name = self.createNewUser(
            inp_login, inp_email, inp_pass, inp_name,
            aux_params=["do_not_logout_admin", "manager_rights"]
        )

        self.closeAdminPanel()
        self.gotoXsm()
        self.gotoXsmActive()
        self.gotoXsmAddPerson()

        person = xsm.Person(self)
        person.input(
            last_name=u"ИксЭсЭмов",
            first_name=u"Юзер",
            patronymic=u"Ламерович",
            email=inp_email,
        )

        self.gotoRoot()
        self.performLogoutFromSite()

        if not self.performLogin(inp_login, inp_pass):
            self.failTest("Cannot login as newly created user. ")

        self.gotoCabinet()
        self.assertBodyTextPresent("XSM")
        card_caption = u"Карточка участника в XSM"
        self.assertBodyTextPresent(card_caption)
        xsm_url_text = person.short_alias()
        self.gotoUrlByLinkText(xsm_url_text)
        self.assertBodyTextPresent(person.full_alias(), "We should get into our XSM person card. ")

        self.gotoRoot()
        self.performLogoutFromSite()

        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUserList()

        self.gotoUrlByPartialLinkText(inp_login, "Click on user name in the list")

        self.assertBodyTextPresent(card_caption, "We should see XSM card link. ")
        self.gotoUrlByLinkText(person.short_alias(), "Click on XSM card link")

        # TODO: here also should be link to user's XSM profile, if any.
