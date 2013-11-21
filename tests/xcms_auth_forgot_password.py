#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthForgotPassword(SeleniumTest):
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
        conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(conf.getPhpErrorCheckFlag())
        
        xtest_common.assertNoInstallerPage(self)
        
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())
            
        self.gotoRoot()
        
        # create new user with ruined memory
        inpLogin = "oblivion_" + random_crap.randomText(6)
        inpEMail = "testsite001@fizlesh.ru"
        inpPass = random_crap.randomText(10)
        inpName = u"Ruined_Memory_" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = xtest_common.createNewUser(self, conf, inpLogin, inpEMail, inpPass, inpName)
        
        print "logging as created user. "
        if not xtest_common.performLogin(self, inpLogin, inpPass):
            raise selenium_test.TestError("Cannot login as newly created user. ")
        
        # logout self 
        xtest_common.performLogoutFromSite(self)

        # we navigate to root page, and see auth panel!
        print "login again and press 'forgot password' button "
        xtest_common.gotoAuthLink(self)
        
        self.fillElementById("reset-email", inpEMail)
        self.fillElementById("question", conf.getForgottenPasswordCaptcha())
        self.clickElementById("reset-submit")
        
        if xtest_common.performLogin(self, inpLogin, inpPass):
            raise selenium_test.TestError("Password was not reset. Old password works. ")

        # set random email to user to avoid problems with duplicate email (may occur only if test fails)
        xtest_common.setUserEmailByAdmin(self, conf, inpLogin, random_crap.randomEmail())


        
        

