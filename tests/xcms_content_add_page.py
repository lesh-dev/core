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

        # avoid spontaneous HTML tags
        self.specChars = random_crap.specialCharsWoAngle # without <>
        #TODO: BUG: remove this spike for Chrome
        self.wordOptions = ["english"]
        
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
        
        pageText = random_crap.randomCrap(10, self.wordOptions, specialChars = self.specChars)
        print "Generated page text: '" + pageText + "'"
        
        pageText = self.fillElementById("edit-text", pageText)
        print "After ins page text: '" + pageText + "'"
        self.clickElementById("edit-submit-top")

        self.clickElementById("edit-preview-top")

        previewElement = "content-text-preview"
        self.assertElementTextById(previewElement, pageText, "preview text does not match entered page text. ")
        
        # add second line
        newPageText = pageText + "\n" + random_crap.randomCrap(10, self.wordOptions, specialChars = self.specChars)
        
        newPageText = self.fillElementById("edit-text", newPageText)
        print "Generated 2-line page text: '" + newPageText + "'"

        self.clickElementById("edit-submit-top")
        self.clickElementById("edit-preview-top")
             
        newPageTextForCheck = newPageText.replace("\n", " ").replace("  ", " ").replace(">>", u"»").replace("<<", u"«").strip()

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
        
        self.testVersions()
                
        self.testDiffAndLongText()
    
    def testVersions(self):
        versionUnoText = "version_0001"
        versionUnoText = self.fillElementById("edit-text", versionUnoText)
        self.clickElementById("edit-submit-top")
        
        versionDosText = "version_0002"
        versionDosText = self.fillElementById("edit-text", versionDosText)
        self.clickElementById("edit-submit-top")

        versionTresText = "version_0003"
        versionTresText = self.fillElementById("edit-text", versionTresText)
        self.clickElementById("edit-submit-top")
        
        self.setOptionValueByIdAndIndex("versions-top", 3)
        self.clickElementByName("set-version") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionUnoText)

        self.setOptionValueByIdAndIndex("versions-top", 1)
        self.clickElementByName("set-version") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionTresText)
        
        self.setOptionValueByIdAndIndex("versions-top", 2)
        self.clickElementByName("set-version") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionDosText)
        

    def testDiffAndLongText(self):
        
        wordNumber = 6
        totalLines = 8
        
        diffLines = [htmlParagraph(random_crap.randomCrap(wordNumber, self.wordOptions, specialChars = self.specChars)) for x in xrange(0,totalLines)]
        
        diffPageText = "\n".join(diffLines)
        
        diffPageText = self.fillElementById("edit-text", diffPageText)

        self.clickElementById("edit-submit-top")
        
        # insert one line 
        insLine = htmlParagraph(random_crap.randomCrap(5, self.wordOptions, specialChars = self.specChars))
        
        diffLines = diffLines[:3] + [insLine] + diffLines[3:5] + diffLines[7:]
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
            replacement = htmlParagraph(random_crap.randomCrap(5, self.wordOptions, specialChars = self.specChars))
            diffPageText = diffPageText.replace(sample, replacement)
        
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

    


