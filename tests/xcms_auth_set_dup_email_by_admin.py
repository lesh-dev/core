#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsAuthSetDuplicateEmailByAdmin(xtest_common.XcmsTest):
    """
    This test checks following functional:
    Add new user and sets him email which is already taken by another user.
    steps:
    create some user A
    create another user B
    set user B's email to email of user A.

    """

    def run(self):

        # step one: create first user
        inpLogin1 = "dup_mail1_" + random_crap.randomText(8)
        inpEMail1 = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpName1 = u"Вася Тестов" + random_crap.randomText(6)

        inpLogin1, inpEMail1, inpPass1, inpName1 = self.createNewUser(inpLogin1, inpEMail1, inpPass1, inpName1, ["do_not_logout_admin"])

        # step 2: create another user
        inpLogin2 = "dup_mail2_" + random_crap.randomText(8)
        inpEMail2 = random_crap.randomEmail()
        inpPass2 = random_crap.randomText(10)
        inpName2 = u"Миша Тестов" + random_crap.randomText(6)

        # create second user without re-login Admin

        inpLogin2, inpEMail2, inpPass2, inpName2 = self.createNewUser(inpLogin2, inpEMail2, inpPass2, inpName2, ["do_not_login_as_admin"])

        print "logging as created first user. "
        if not self.performLogin(inpLogin1, inpPass1):
            self.failTest("Cannot login as newly created user One. ")

        self.performLogoutFromSite()

        print "logging as created second user. "
        if not self.performLogin(inpLogin2, inpPass2):
            self.failTest("Cannot login as newly created user Two. ")

        self.performLogoutFromSite()

        # login as admin, enter user profile and change some fields.

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "enter user profile in admin CP"

        self.gotoUrlByPartialLinkText(inpLogin2)

        self.assertElementValueById("name-input", inpName2)
        self.assertElementValueById("email-input", inpEMail2)

        # try to hack email
        inpEMail2new = inpEMail1

        inpEMail2new = self.fillElementById("email-input", inpEMail2new)
        print "new email 2: ", inpEMail2new

        self.clickElementById("update_user-submit")

        self.assertBodyTextPresent(u"уже существует")

        # self.performLogoutFromAdminPanel()
