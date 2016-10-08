#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
#import selenium_test


class XcmsAuthForgotPassword(xtest_common.XcmsTest):
    """
    This test checks user add functional.
    It does following steps:
    * login as root user
    * navigate to user control panel
    * add random user
    * login as new user
    * logout
    * open login window
    * press 'forgot password' button
    * check e-mail (manually)
    * test auto-gen password (manually)
    """

    def run(self):
        self.ensure_logged_off()

        self.gotoRoot()

        inpEMail = self.m_conf.getValidEmail(1)

        self.removePreviousUsersWithTestEmail(inpEMail)

        # create new user with ruined memory
        inpLogin = "oblivion_" + random_crap.randomText(6)

        inpPass = random_crap.randomText(10)
        inpName = u"Ruined_Memory_" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)

        print "logging as created user. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login as newly created user. ")

        # logout self
        self.performLogoutFromSite()

        # we navigate to root page, and see auth panel!
        self.logAdd("login again and press 'forgot password' button ")
        self.gotoAuthLink()

        self.fillElementById("reset-email-input", inpEMail)
        self.fillElementById("question-input", self.m_conf.getForgottenPasswordCaptcha())
        self.clickElementById("reset_password-submit")

        if self.performLogin(inpLogin, inpPass):
            self.failTest("Password was not reset. Old password works fine. ")

        # set random email to user to avoid problems with duplicate email (may occur only if test fails)
        self.setUserEmailByAdmin(inpLogin, random_crap.randomEmail())
