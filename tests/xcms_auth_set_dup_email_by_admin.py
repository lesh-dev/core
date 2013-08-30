#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthSetDuplicateEmailByAdmin(SeleniumTest):
    """
    This test checks following functional:
    Add new user and sets him email which is already taken by another user.
    steps:
    create some user A
    create another user B
    set user B's email to email of user A.
    
    """
    
    def run(self):
        self.setAutoPhpErrorChecking(True)
        
        xtest_common.assertNoInstallerPage(self)
        
        conf = XcmsTestConfig()
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())
        
        # step one: create first user
        inpLogin1 = "dup_mail1_" + random_crap.randomText(8)
        inpEMail1 = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpName1 = u"Вася Тестов" + random_crap.randomText(6)
        
        inpLogin1, inpEMail1, inpPass1, inpName1 = xtest_common.createNewUser(self, conf, inpLogin1, inpEMail1, inpPass1, inpName1, ["do_not_logout_admin"])
        
        # step 2: create another user
        inpLogin2 = "dup_mail2_" + random_crap.randomText(8)
        inpEMail2 = random_crap.randomEmail()
        inpPass2 = random_crap.randomText(10)
        inpName2 = u"Миша Тестов" + random_crap.randomText(6)
        
        # create second user without re-login Admin
        
        inpLogin2, inpEMail2, inpPass2, inpName2 = xtest_common.createNewUser(self, conf, inpLogin2, inpEMail2, inpPass2, inpName2, ["do_not_login_as_admin"])
        
        print "logging as created first user. "
        if not xtest_common.performLogin(self, inpLogin1, inpPass1):
            raise selenium_test.TestError("Cannot login as newly created user One. ")
        
        xtest_common.performLogoutFromSite(self)        
        
        print "logging as created second user. "
        if not xtest_common.performLogin(self, inpLogin2, inpPass2):
            raise selenium_test.TestError("Cannot login as newly created user Two. ")
        
        xtest_common.performLogoutFromSite(self)        
        
        # login as admin, enter user profile and change some fields.
        
        xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
        
        xtest_common.gotoAdminPanel(self)
        xtest_common.gotoUserList(self)
        
        print "enter user profile in admin CP"
        
        self.gotoUrlByPartialLinkText(inpLogin2)
        
        self.assertElementValueById("name-input", inpName2)
        self.assertElementValueById("email-input", inpEMail2)
        
        # try to hack email
        inpEMail2new = inpEMail1
        
        inpEMail2new = self.fillElementById("email-input", inpEMail2new)
        print "new email 2: ", inpEMail2new
        
        self.clickElementById("update_user")
        
        self.assertBodyTextPresent(u"уже существует")
        
        #xtest_common.performLogoutFromAdminPanel(self)
        
        