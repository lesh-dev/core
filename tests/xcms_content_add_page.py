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

        #self.gotoRoot()
        #self.wait(1)
        #print "func: ", self.m_driver.title;
        
        #print "page title by tag: ", self.getPageTitle()
        #print self.getPageSource()
        #print "tag: ", self.m_driver.find_element_by_xpath("/html/head").find_elements_by_xpath("*")[4].tag_name
        #print "text: ", self.m_driver.find_element_by_xpath("/html/head").find_elements_by_xpath("*")[4].find_elements_by_xpath("*")[0].text
        #print "page title: ", self.getElementContent("/html/head")
        #self.failTest("stop")

        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())


            
        xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
        
        xtest_common.gotoAdminPanel(self)
        

        
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

        defaultPageType = self.getOptionValueById("create-pagetype-selector")
        
        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)
        
        self.clickElementById("create-submit")
        
        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)
        
        pageText = random_crap.randomCrap(10)
        
        pageText = self.fillElementById("edit-text", pageText)
        self.clickElementById("edit-submit-top")

        self.clickElementById("edit-preview-top")

        contentDiv = "/html/body/div/div[@class='content']"

        print "DIV CONTENT:"
        print self.getElementContent(contentDiv)
        print "DIV CONTENT END"

        self.assertTextPresent(contentDiv, pageText, "preview text does not match entered text. ")
        
        # add second line
        newPageText = pageText + "\n" + random_crap.randomCrap(10)
        
        newpageText = self.fillElementById("edit-text", newPageText)

        self.clickElementById("edit-submit-top")
        self.clickElementById("edit-preview-top")
        
        print "DIV CONTENT:"
        print self.getElementContent(contentDiv)
        print "DIV CONTENT END"
        
        newPageTextForCheck = newPageText.replace("\n", " ")

        self.assertTextPresent(contentDiv, newPageTextForCheck, "preview text on text change does not match entered text. ")

        self.gotoUrlByLinkText(u"Свернуть редактор")
        
        self.assertBodyTextPresent(u"Личный кабинет")
        # click on menu.
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertBodyTextPresent(newPageTextForCheck, "page text on text change does not match entered text. ")
        pageTitle = self.getPageTitle()
        if inpMenuTitle not in pageTitle:
            self.failTest("Menu title text does not appear in page title. ") # WTF?? TODO: why Menu title, not page title?

        #self.assertBodyTextPresent(inpPageSubheader, "page subheader does not match entered text. ")

