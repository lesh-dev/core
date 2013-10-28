#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

def htmlParagraph(x):
    return "<p>" + x + "</p>"

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
        #print "page title: ", self.getElementText("/html/head")
        #self.failTest("stop")

        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())


            
        xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
        
        xtest_common.gotoAdminPanel(self)
        

        parentPage = u"Главная"
        
        self.gotoUrlByLinkText(parentPage)
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

        previewElement = "content-text-preview"
        self.assertElementTextById(previewElement, pageText, "preview text does not match entered page text. ")
        
        # add second line
        newPageText = pageText + "\n" + random_crap.randomCrap(10)
        
        newPageText = self.fillElementById("edit-text", newPageText)

        self.clickElementById("edit-submit-top")
        self.clickElementById("edit-preview-top")
             
        newPageTextForCheck = newPageText.replace("\n", " ")

        self.assertElementTextById(previewElement, newPageTextForCheck, "preview text on text change does not match entered text. ")

        self.gotoUrlByLinkText(u"Свернуть редактор")
        
        self.assertBodyTextPresent(u"Личный кабинет")
        # click on menu.
        
        self.gotoUrlByLinkText(parentPage)
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertElementTextById("content-text", newPageTextForCheck, "page text after reopening editor does not match entered text. ")
        
        pageTitle = self.getPageTitle()
        if inpMenuTitle not in pageTitle:
            self.failTest("Menu title text does not appear in page title. ") # WTF?? TODO: why Menu title, not page title?

        #self.assertBodyTextPresent(inpPageSubheader, "page subheader does not match entered text. ")

        self.gotoUrlByLinkText(u"Редактировать")
        
        diffLines = [htmlParagraph(random_crap.randomCrap(7)) for x in xrange(0,12)]
        
        diffPageText = "\n".join(diffLines)

        print "before fill"
        
        diffPageText = self.fillElementById("edit-text", diffPageText)
        print "after fill"
        self.clickElementById("edit-submit-top")
        
        diffLines = diffLines[:3] + [htmlParagraph(random_crap.randomCrap(5))] + diffLines[3:6] + diffLines[7:]
        diffPageText = "\n".join(diffLines)

        diffPageText = self.fillElementById("edit-text", diffPageText)
        self.clickElementById("edit-submit-top")

        diffLines = diffLines[:-1]
        diffPageText = "\n".join(diffLines)

        diffPageText = self.fillElementById("edit-text", diffPageText)
        self.clickElementById("edit-submit-top")
        
        pageWords = diffPageText.split()
        
        sampleWords = pageWords[5:8] + pageWords[24:27] + pageWords[30:32]
        for sample in sampleWords:
            diffPageText = diffPageText.replace(sample, random_crap.randomCrap(2))
        
        diffPageText = self.fillElementById("edit-text", diffPageText)
        self.clickElementById("edit-submit-top")
        
        self.gotoUrlByLinkText(u"Свернуть редактор")

        #print "-"*20, "before:"
        #print diffPageText
        #print "-"*20
        diffPageTextForCheck = diffPageText.replace("<p>", "").replace("\n", " ").replace("</p> ", "\n").replace("</p>", "\n").strip()
        #print "-" * 20
        #print diffPageTextForCheck
        #print "-" * 20, "actual:"
        #print self.getElementTextById("content-text")
        #print "-" * 20
        
        self.assertElementTextById("content-text", diffPageTextForCheck, "real page text does not match entered text. ")
        
    


