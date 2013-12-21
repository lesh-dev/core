#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap, time

def htmlParagraph(x):
    return "<p>" + x + "</p>"

def linesToHtml(lineArray):
    return "\n".join([htmlParagraph(x) for x in lineArray])

class XcmsContentAddPage(xtest_common.XcmsTest):
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
        
        self.testBaseEditing()

        self.testVersions()

        self.testDiffAndLongText()
        
        self.testAlias()
        
        self.testBadAlias()
        
    def testBaseEditing(self):

        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        
        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoUrlByLinkText(u"Подстраница")

        inpPageDir = "test_page_" + random_crap.randomText(8);
        inpMenuTitle = "menu_title_" + random_crap.randomText(8);
        inpPageHeader = "page_header_" + random_crap.randomText(8);
        inpAlias = "new/page/alias/" + random_crap.randomText(8);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);
        
        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-submit")
        
        #TODO: wait for fixing of bug with automatic alias rebuildAliases

        self.logAdd("Rebuilding aliases for first time to w/a bug ")
        self.rebuildAliases()
        #self.wait(2)

        #self.logAdd("Opening editor again after redirection. ")
        #self.gotoEditPageInPlace()

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader
        
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

        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(self.m_parentPage)
        self.logAdd("Clicking on new page menu item. ")
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertElementTextById("content-text", newPageTextForCheck, "page text after reopening editor does not match entered text. ")
        self.assertElementTextById("content-header", self.m_pageHeader, "page header does not match entered header. ")

        if inpMenuTitle not in self.getPageTitle():
            self.failTest("Menu title text does not appear in page title after going to the page by menu. ")

    def testVersions(self):
        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoUrlByLinkText(self.m_menuTitle)
        
        self.gotoEditPageInPlace()
                        
        versionUnoText = "version_0001"
        versionUnoText = self.fillElementById("edit-text", versionUnoText)
        self.clickElementById("edit-submit-top")
        self.wait(2)

        versionDosText = "version_0002"
        versionDosText = self.fillElementById("edit-text", versionDosText)
        self.clickElementById("edit-submit-top")
        self.wait(2)

        versionTresText = "version_0003"
        versionTresText = self.fillElementById("edit-text", versionTresText)
        self.clickElementById("edit-submit-top")
        self.wait(2)

        self.setOptionValueByIdAndIndex("versions-top", 3)
        self.clickElementById("set-version-top") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionUnoText)

        self.setOptionValueByIdAndIndex("versions-top", 1)
        self.clickElementById("set-version-top") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionTresText)

        self.setOptionValueByIdAndIndex("versions-top", 2)
        self.clickElementById("set-version-top") # Смотреть версию
        self.wait(1)
        self.assertElementTextById("edit-text", versionDosText)
    
    def testDiffAndLongText(self):

        self.logAdd("test diff engine. ")
        self.wait(2)
        
        wordNumber = 7
        totalLines = 8

        origLines = [random_crap.randomCrap(wordNumber, self.wordOptions, specialChars = self.specChars) for x in xrange(0, totalLines)]

        pageText = linesToHtml(origLines)

        pageText = self.fillElementById("edit-text", pageText)

        print "diff test page text original: "
        print pageText
        print "-" * 30

        self.clickElementById("edit-submit-top")

        # insert one line
        insLine = random_crap.randomCrap(wordNumber, self.wordOptions, specialChars = self.specChars)

        # remove some lines inside
        newLines = origLines[:3] + [insLine] + origLines[3:5] + origLines[7:]
        pageText = linesToHtml(newLines)

        pageText = self.fillElementById("edit-text", pageText)
        
        print "diff test page new text: "
        print pageText
        print "-" * 30

        self.clickElementById("edit-submit-top")

        # cut last line
        newLines = newLines[:-1]
        
        pageText = linesToHtml(newLines)

        pageText = self.fillElementById("edit-text", pageText)
        self.clickElementById("edit-submit-top")

        pageWords = (" ".join(newLines)).split()
        
        print "word count ", len(pageWords)

        sampleWords = pageWords[5:9] + pageWords[24:27] + pageWords[30:32]
        for sample in sampleWords:
            print "replacing word: ", sample
            replacement = random_crap.randomCrap(4, self.wordOptions, specialChars = self.specChars)
            print "replacement: ", replacement
            pageText = pageText.replace(sample, replacement)

        print "diff test page new text after word-replacement: "
        print pageText
        print "-" * 30

        pageText = self.fillElementById("edit-text", pageText)
        
        self.clickElementById("edit-submit-top")

        self.gotoCloseEditor()

        realPageText = pageText.replace("<p>", "").replace("\n", " ").replace("</p> ", "\n").replace("</p>", "\n").strip()

        print "real page text: "
        print realPageText
        print "-" * 30

        self.assertElementTextById("content-text", realPageText, "real page text does not match entered text. ")

    def updateAliases(self):
        self.logAdd("Updating aliases. ")
        self.clickElementByName("change-alias")
        self.assertBodyTextPresent(u"Список alias-ов обновлён")
        self.wait(2, "wait for redirection")
        
    def gotoAlias(self, alias):
        self.logAdd("Going to the page via alias " + alias)
        self.gotoPage("/" + alias)
        
    def testAlias(self):
        self.logAdd("test aliases")
        
        self.gotoEditPageInPlace()
        
        # edit alias
        self.gotoUrlByLinkText(self.m_pageAlias)
        self.assertBodyTextPresent("Alias")
        
        inpAlias = "changed/newpage/alias/" + random_crap.randomText(8);

        inpAlias = self.fillElementByName("alias", inpAlias)
        self.m_pageAlias = inpAlias
        
        self.updateAliases()
        
        # self.rebuildAliases()
        self.gotoAlias(self.m_pageAlias)

        if self.m_menuTitle not in self.getPageTitle():
            self.failTest("Page/menu title text does not appear in page title after going to page by alias after alias change. ")
        
        self.assertElementTextById("content-header", self.m_pageHeader, "page header does not match entered header. ")
        
    def testBadAlias(self):

        self.logAdd("test bad aliases")
        self.gotoEditPageInPlace()

        self.gotoUrlByLinkText(self.m_pageAlias)
        self.assertBodyTextPresent("Alias")
        
        inpAlias = "    " # evil hack
        
        inpAlias = self.fillElementByName("alias", inpAlias)
        self.m_pageAlias = inpAlias

        self.updateAliases()
            
        #self.gotoCloseEditor()
                
        self.gotoAdminPanel()
        self.assertUrlPresent(u"Подстраница", "We should successfully enter admin panel, but we cannot see button to create new subpage. ")
        