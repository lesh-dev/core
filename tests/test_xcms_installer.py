#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class TestXcmsInstaller(SeleniumTest):
    """
    This test checks XCMS installator.
    It does following steps:
    * navigates to setup form
    * submits form with default values
    * checks if 'installation complete' message appeared
    """
    
    def run(self):
        self.gotoRoot()
        self.assertSourceTextPresent(["XCMS installer", u"Установка XCMS"])
        # very meaningful name...
        self.clickElementByName("submit_variables")
        self.assertSourceTextPresent(u"Установка завершена!")
        self.gotoUrlByLinkText(u"Перейти к сайту")
        
        # set notifications - once for all tests to avoid broadcast notifications to all production server admins.
        
        conf = XcmsTestConfig()
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())

        
    