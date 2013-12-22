#!/usr/bin/python
# -*- coding: utf8 -*-

import random_crap, xtest_common

class TestXcmsInstaller(xtest_common.XcmsTestWithConfig):
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
               
        self.setTestNotifications()
        self.checkTestNotifications()

    def checkDocType(self):
        self.logAdd("DOCTYPE checking disabled for installer test. ", "warning")
        

        
    