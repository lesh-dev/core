#!/usr/bin/env python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsAuthCabinetEmailChange(xtest_common.XcmsTest):
    """
    add two users with different e-mails
    enter cabinet and change e-mail to another good email
    test notification in mailbox (manually)
    set user2's e-mail to user1
    check if user1's email was not changed actually
    login as user2
    """

    def run(self):

        inpLogin1 = "cab_email_" + random_crap.randomText(6)
        inpLogin2 = "cab_email_" + random_crap.randomText(6)
        inpEMail1 = random_crap.randomEmail()
        inpEMail2 = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpPass2 = random_crap.randomText(10)
        inpName1 = u"Вася " + random_crap.randomText(6)
        inpName2 = u"Петя " + random_crap.randomText(6)

        inpLogin1, inpEMail1, inpPass1, inpName1 = self.createNewUser(inpLogin1, inpEMail1, inpPass1, inpName1)

        inpLogin2, inpEMail2, inpPass2, inpName2 = self.createNewUser(inpLogin2, inpEMail2, inpPass2, inpName2)

        print "logging as first created user. "
        if not self.performLogin(inpLogin1, inpPass1):
            self.failTest("Cannot login as newly created first user. ")

        self.gotoCabinet()

        print "test good email"
        newGoodEMail = self.m_conf.getValidEmail(2)

        self.fillElementById("email-input", newGoodEMail)
        self.clickElementById("update_me-submit")

        badMailMsg = u"пользователь с такой почтой"
        dataUpdatedMsg = u"Данные обновлены успешно"

        self.assertBodyTextNotPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextPresent(dataUpdatedMsg)

        print "Ok. Please check your mailbox for notification. "

        print "test another good random email"
        newGoodEMail = random_crap.randomEmail()

        newGoodEMail = self.fillElementById("email-input", newGoodEMail)
        self.clickElementById("update_me-submit")

        self.assertBodyTextNotPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextPresent(dataUpdatedMsg)

        print "And now test bad e-mail. "

        newBadEMail = inpEMail2

        self.fillElementById("email-input", newBadEMail)
        self.clickElementById("update_me-submit")

        self.assertBodyTextPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextNotPresent(dataUpdatedMsg)

        self.performLogoutFromAdminPanel()

        print "logging as first created user again. "
        if not self.performLogin(inpLogin1, inpPass1):
            self.failTest("Cannot login again as newly created first user. ")

        self.gotoCabinet()

        self.assertElementValueById("email-input", newGoodEMail, "Email should remain unchanged after 1st change")

        self.performLogoutFromAdminPanel()

        print "logging as second created user. "
        if not self.performLogin(inpLogin2, inpPass2):
            self.failTest("I was not able to login as second user. ")


