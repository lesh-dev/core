#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

import xtest_common
import random_crap


class XcmsAuthAddNewUser(xtest_common.XcmsTest):
    """
    This test checks user add functional.
    It does following steps:
    * login as root user
    * navigate to user control panes
    * add random user
    * login as new user
    * change user password
    * logout
    * login with incorrect password
    * change password
    * login again with changed password
    """

    def run(self):
        self.ensure_logged_off()

        self.gotoRoot()

        # first, login as admin
        inpLogin = "an_test_user_" + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpPass = random_crap.random_text(10)
        inpName = u"Вася Пупкин" + random_crap.random_text(6)

        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)

        logging.info("logging as created user. ")
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login as newly created user. ")

        # logout self
        self.performLogoutFromSite()

        # test wrong auth
        logging.info("logging in as created user with incorrect password ")
        if self.performLogin(inpLogin, "wrong_pass" + inpPass):
            self.failTest("I'm able to login with incorrect password. Auth is broken. ")

        # and now, test bug with remaining cookies:
        # we navigate to root page, and see auth panel!
        logging.info("logging in again as created user. ")
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login again as newly created user. ")

        self.gotoCabinet()

        # let's try to change password.
        self.gotoUrlByLinkText(u"Сменить пароль")

        new_pass = inpPass + "_new"
        self.fillElementById("old_passwd-input", inpPass)
        new_pass1 = self.fillElementById("new_passwd-input", new_pass)
        new_pass2 = self.fillElementById("new_passwd_confirm-input", new_pass)
        if new_pass1 != new_pass2:
            raise RuntimeError("Unpredicted input behavior on password change")
        new_pass = new_pass1
        self.clickElementByName("change_my_password")
        self.assertBodyTextPresent(u"Пароль успешно изменён")

        self.performLogoutFromAdminPanel()

        print "logging again as created user with new password"
        if not self.performLogin(inpLogin, new_pass):
            self.failTest("Cannot login again as newly created user with changed password. ")

        # logout self
        self.performLogoutFromSite()

        # and now let's edit user profile.

        print "now let's edit profile. Logging 3-rd time with new password"
        if not self.performLogin(inpLogin, new_pass):
            self.failTest("Cannot login again for profile info change. ")

        self.gotoCabinet()
        # navigate to user profile which is just user login
        # TODO: BUG, make separate links

        self.gotoUrlByPartialLinkText(inpLogin)

        self.assertBodyTextPresent(self.getWelcomeMessage(inpLogin))

        name_ele = "name-input"
        email_ele = "email-input"

        currentDisplayName = self.getElementValueById(name_ele)
        self.assert_equal(
            currentDisplayName, inpName,
            "Display name in user profile does not match name entered on user creation. "
        )

        currentEMail = self.getElementValueById(email_ele)
        self.assert_equal(
            currentEMail, inpEMail,
            "User e-mail in user profile does not match e-mail entered on user creation. "
        )

        newName = u"Петя Иванов" + random_crap.random_text(6)
        newEMail = random_crap.randomEmail()

        newName = self.fillElementById(name_ele, newName)

        print "New user display name is ", newName
        newEMail = self.fillElementById(email_ele, newEMail)
        print "New user e-mail is ", newEMail

        self.clickElementById("update_me-submit")

        self.performLogoutFromAdminPanel()

        print "now let's login again and see updated profile."
        if not self.performLogin(inpLogin, new_pass):
            self.failTest("Cannot login after profile info change. ")

        self.gotoCabinet()
        # navigate to user profile which is just user login
        self.gotoUrlByLinkText(inpLogin)
        self.assertBodyTextPresent(u"Привет, " + inpLogin)

        currentDisplayName = self.getElementValueById(name_ele)
        self.assert_equal(
            currentDisplayName, newName,
            "Display name in user profile does not match changed user name. "
        )

        currentEMail = self.getElementValueById(email_ele)
        self.assert_equal(currentEMail, newEMail, "User e-mail in user profile does not match changed user e-mail. ")
