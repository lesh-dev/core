#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import user
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

        self.goto_root()

        inp_email = self.m_conf.getValidEmail(1)

        self.removePreviousUsersWithTestEmail(inp_email)

        # create new user with ruined memory
        inp_login = "oblivion_" + random_crap.random_text(6)

        inp_pass = random_crap.random_text(10)
        inp_name = u"Ruined_Memory_" + random_crap.random_text(6)

        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            email=inp_email,
            password=inp_pass,
            name=inp_name,
            random=False,
        )

        print "logging as created user. "
        if not self.perform_login(u.login, u.password):
            self.failTest("Cannot login as newly created user. ")

        # logout self
        self.performLogoutFromSite()

        # we navigate to root page, and see auth panel!
        self.logAdd("login again and press 'forgot password' button ")
        self.gotoAuthLink()

        self.fillElementById("reset-email-input", u.email)
        self.fillElementById("question-input", self.m_conf.getForgottenPasswordCaptcha())
        self.clickElementById("reset_password-submit")

        if self.perform_login(u.login, u.password):
            self.failTest("Password was not reset. Old password works fine. ")

        # set random email to user to avoid problems with duplicate email (may occur only if test fails)
        self.setUserEmailByAdmin(u.login, random_crap.randomEmail())
