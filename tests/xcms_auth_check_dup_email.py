#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthCheckDupEmail(SeleniumTest):
    """
    add two users with identical e-mails. 
    """
    
    def run(self):
        self.setAutoPhpErrorChecking(True)
        
        xtest_common.assertNoInstallerPage(self)
        
        conf = XcmsTestConfig()
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())

        inpLogin1 = "dup_email_" + random_crap.randomText(8)
        inpLogin2 = "dup_email_" + random_crap.randomText(8)
        inpEMail = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpPass2 = random_crap.randomText(10)
        inpName1 = u"Вася " + random_crap.randomText(6)
        inpName2 = u"Петя " + random_crap.randomText(6)

        inpLogin1, inpEMail, inpPass1, inpName1 = xtest_common.createNewUser(self, conf, inpLogin1, inpEMail, inpPass1, inpName1)

        inpLogin2, inpEMail, inpPass2, inpName2 = xtest_common.createNewUser(self, conf, inpLogin2, inpEMail, inpPass2, inpName2, ["do_not_validate"])

        self.assertBodyTextNotPresent(u"Пользователь успешно создан", "We should get error about duplicate e-mails. ")
        
        xtest_common.performLogout(self)
        
        print "logging as first created user. "
        if not xtest_common.performLogin(self, inpLogin1, inpPass1):
            raise selenium_test.TestError("Cannot login as newly created first user. ")

        xtest_common.performLogout(self)

        print "try logging as second created user. "
        if xtest_common.performLogin(self, inpLogin2, inpPass2):
            raise selenium_test.TestError("I was able to login as second user with duplicate e-mail. ")


