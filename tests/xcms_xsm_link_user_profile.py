#!/usr/bin/python
# -*- coding: utf8 -*-

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
        inpLogin = "xsm_link_" + random_crap.randomText(6)
        inpEMail = random_crap.randomEmail()
        inpPass = random_crap.randomText(8)
        inpName = u"XSM-Юзер-" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(
            inpLogin, inpEMail, inpPass, inpName,
            aux_params=["do_not_logout_admin", "manager_rights"]
        )

        self.closeAdminPanel()
        self.gotoXsm()
        self.gotoXsmActive()
        self.gotoXsmAddPerson()

        # generate
        inpLastName = u"ИксЭсЭмов" + random_crap.randomText(4)
        inpFirstName = u"Юзер_" + random_crap.randomText(3)
        inpMidName = u"Ламерович_" + random_crap.randomText(3)
        inpEMailXsm = inpEMail

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpEMailXsm = self.fillElementById("email-input", inpEMailXsm)

        if inpEMail != inpEMailXsm:
            self.failTest("Cannot create user with identical email. ")

        self.clickElementById("update-person-submit")

        self.gotoRoot()
        self.performLogoutFromSite()

        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login as newly created user. ")

        self.gotoCabinet()
        self.assertBodyTextPresent("XSM")
        cardCaption = u"Карточка участника в XSM"
        self.assertBodyTextPresent(cardCaption)
        xsmUrlText = xtest_common.shortAlias(inpLastName, inpFirstName)
        self.gotoUrlByLinkText(xsmUrlText)
        xsmAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        #self.checkPersonAliasInPersonView(xsmAlias, "We should get into our XSM person card. ")
        self.assertBodyTextPresent(xsmAlias, "We should get into our XSM person card. ")

        self.gotoRoot()
        self.performLogoutFromSite()

        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUserList()

        self.gotoUrlByPartialLinkText(inpLogin, "Click on user name in the list")

        self.assertBodyTextPresent(cardCaption, "We should see XSM card link. ")
        xsmLinkAlias = xtest_common.shortAlias(inpLastName, inpFirstName)

        self.gotoUrlByLinkText(xsmLinkAlias, "Click on XSM card link")

        # TODO: here also should be link to user's XSM profile, if any.
