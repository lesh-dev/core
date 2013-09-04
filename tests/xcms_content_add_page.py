#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsContentAddPage(SeleniumTest):
    """
    This test checks user add functional.
    It does following steps:
    * login as root user (in future - site editor)
    * add new subpage
    * edit new subpage some times
    * load previous version
    """
            
    def run(self):
        conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(conf.getPhpErrorCheckFlag())
        xtest_common.assertNoInstallerPage(self)
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())
            
        xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
        
        xtest_common.gotoAdminPanel()
        
        self.gotoUrlByLinkText(u"Главная")
        self.gotoUrlByLinkText(u"Подстраница")
        
        inpPageDir = "test_page_" + random_crap.randomText(8);
        inpMenuTitle = "menu_title_" + random_crap.randomText(8);
        inpPageTitle = "page_title_" + random_crap.randomText(8);
        inpPageSubheader = "page_sub_header_" + random_crap.randomText(8);
        
        inpPageDir = self.fillElementByName("create-name", inpPageDir);
        inpMenuTitle = self.fillElementByName("menu-title", inpMenuTitle);
        inpPageTitle = self.fillElementByName("header", inpPageTitle);
        inpPageSubheader = self.fillElementByName("subheader", inpPageSubheader);

        if self.getOptionValueById("create-pagetype") != "content":
            self.failTest("Default selected page type is not 'content'. ")
        
        self.clickElementById("create-submit")
        

