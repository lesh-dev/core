#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import selenium_test

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

    def removePreviousUsersWithTestEmails(self):
        
        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUserList()
        
        emailToDelete = self.m_conf.getValidEmail1()
        
        while True:
            try:
                userUrl = self.getUrlByLinkText(emailToDelete, ["partial"])
                self.logAdd("Test user found, removing it. ")
                self.gotoSite(userUrl)
                self.clickElementById("check_delete_user")
                self.assertBodyTextPresent(u"Вы точно уверены, что хотите удалить этого пользователя?")
                self.clickElementById("delete_user")
                self.assertBodyTextPresent(u"Пользователь удалён.")
                
            except selenium_test.ItemNotFound as e:
                self.logAdd("Users with test email not found, continuing. ")
                break

        self.logAdd("Test users (old crap) removed, logging out. ")
        self.performLogoutFromAdminPanel()
        
    def run(self):
        self.gotoRoot()
        
        self.removePreviousUsersWithTestEmails()

        # create new user with ruined memory
        inpLogin = "oblivion_" + random_crap.randomText(6)

        inpEMail = self.m_conf.getValidEmail1()

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
        self.clickElementById("reset-submit")

        if self.performLogin(inpLogin, inpPass):
            self.failTest("Password was not reset. Old password works fine. ")

        # set random email to user to avoid problems with duplicate email (may occur only if test fails)
        self.setUserEmailByAdmin(inpLogin, random_crap.randomEmail())
