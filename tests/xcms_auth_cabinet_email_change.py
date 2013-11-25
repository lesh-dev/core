#!/usr/bin/env python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthCabinetEmailChange(SeleniumTest):
    """
    add two users with different e-mails
    enter cabinet and change e-mail to another good email
    test notification in mailbox (manually)
    set user2's e-mail to user1
    check if user1's email was not changed actually
    login as user2
    """

    def run(self):
        self.setAutoPhpErrorChecking(True)

        xtest_common.assertNoInstallerPage(self)

        conf = XcmsTestConfig()
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())

        inpLogin1 = "cab_email_" + random_crap.randomText(6)
        inpLogin2 = "cab_email_" + random_crap.randomText(6)
        inpEMail1 = random_crap.randomEmail()
        inpEMail2 = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpPass2 = random_crap.randomText(10)
        inpName1 = u"Вася " + random_crap.randomText(6)
        inpName2 = u"Петя " + random_crap.randomText(6)

        inpLogin1, inpEMail1, inpPass1, inpName1 = xtest_common.createNewUser(self, conf, inpLogin1, inpEMail1, inpPass1, inpName1)

        inpLogin2, inpEMail2, inpPass2, inpName2 = xtest_common.createNewUser(self, conf, inpLogin2, inpEMail2, inpPass2, inpName2)

        print "logging as first created user. "
        if not xtest_common.performLogin(self, inpLogin1, inpPass1):
            raise selenium_test.TestError("Cannot login as newly created first user. ")
        
        xtest_common.gotoCabinet(self)

        print "test good email"
        newGoodEMail = "testsite002@fizlesh.ru"
        
        newGoodEMail = self.fillElementById("email-input", newGoodEMail)
        self.clickElementById("update_me")

        badMailMsg = u"пользователь с такой почтой"
        dataUpdatedMsg = u"Данные обновлены успешно"
        
        self.assertBodyTextNotPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextPresent(dataUpdatedMsg)
        
        print "Ok. Please check your mailbox for notification. "

        print "test another good random email"
        newGoodEMail = random_crap.randomEmail()
        
        newGoodEMail = self.fillElementById("email-input", newGoodEMail)
        self.clickElementById("update_me")

        self.assertBodyTextNotPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextPresent(dataUpdatedMsg)
    
        print "And now test bad e-mail. "
        
        newBadEMail = inpEMail2
        
        newBadEMail = self.fillElementById("email-input", newBadEMail)
        self.clickElementById("update_me")
        
        self.assertBodyTextPresent(badMailMsg)
        self.assertBodyTextNotPresent("exception")
        self.assertBodyTextNotPresent(dataUpdatedMsg)

        xtest_common.performLogoutFromAdminPanel(self)
        
        print "logging as first created user again. "
        if not xtest_common.performLogin(self, inpLogin1, inpPass1):
            raise selenium_test.TestError("Cannot login again as newly created first user. ")
        
        xtest_common.gotoCabinet(self)
        
        self.assertElementValueById("email-input", newGoodEMail, "Email should remain unchanged after 1st change")

        xtest_common.performLogoutFromAdminPanel(self)

        print "logging as second created user. "
        if not xtest_common.performLogin(self, inpLogin2, inpPass2):
            raise selenium_test.TestError("I was not able to login as second user. ")


