#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsAuthCheckDupLogin(xtest_common.XcmsTest):
    """
    add two users with identical logins.
    """

    def run(self):

        # first, login as admin
        inpLogin = "dup_user_" + random_crap.random_text(8)
        inpEMail1 = random_crap.randomEmail()
        inpEMail2 = random_crap.randomEmail()
        inpPass1 = random_crap.random_text(10)
        inpPass2 = random_crap.random_text(10)
        inpName1 = u"Вася " + random_crap.random_text(6)
        inpName2 = u"Петя " + random_crap.random_text(6)

        inpLogin, inpEMail1, inpPass1, inpName1 = self.createNewUser(inpLogin, inpEMail1, inpPass1, inpName1)

        inpLogin, inpEMail2, inpPass2, inpName2 = self.createNewUser(inpLogin, inpEMail2, inpPass2, inpName2, ["do_not_validate"])

        self.assertBodyTextNotPresent(u"Пользователь '" + inpLogin + u"' успешно создан")

        self.performLogout()

        self.logAdd("logging as created first user. ")
        if not self.performLogin(inpLogin, inpPass1):
            self.failTest("Cannot login as newly created user. ")

        # logout self
        self.performLogout()

        print "try logging as created second user. "
        if self.performLogin(inpLogin, inpPass2):
            self.failTest("I am able to login as 'second' user with duplicate login and new password. ")



