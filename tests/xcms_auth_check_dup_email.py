#!/usr/bin/env python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsAuthCheckDupEmail(xtest_common.XcmsTest):
    """
    add two users with identical e-mails.
    """

    def run(self):

        inpLogin1 = "dup_email_" + random_crap.random_text(8)
        inpLogin2 = "dup_email_" + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpPass1 = random_crap.random_text(10)
        inpPass2 = random_crap.random_text(10)
        inpName1 = u"Вася " + random_crap.random_text(6)
        inpName2 = u"Петя " + random_crap.random_text(6)

        inpLogin1, inpEMail, inpPass1, inpName1 = self.createNewUser(inpLogin1, inpEMail, inpPass1, inpName1)

        inpLogin2, inpEMail, inpPass2, inpName2 = self.createNewUser(inpLogin2, inpEMail, inpPass2, inpName2, ["do_not_validate"])

        self.assertBodyTextNotPresent(u"Пользователь '" + inpLogin2 + u"' успешно создан", "We should get error about duplicate e-mails. ")

        self.performLogout()

        print "logging as first created user. "
        if not self.performLogin(inpLogin1, inpPass1):
            self.failTest("Cannot login as newly created first user. ")

        self.performLogout()

        print "try logging as second created user. "
        if self.performLogin(inpLogin2, inpPass2):
            self.failTest("I was able to login as second user with duplicate e-mail. ")


