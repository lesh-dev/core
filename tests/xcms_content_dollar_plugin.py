#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap

def slashify(line):
    return "".join([x * 2 if x == "\\" else x for x in line])

class XcmsContentDollarPlugin(xtest_common.XcmsTest):
    """
    This test checks content editing - dollar plugin functionality.
    Steps:
    * login as site editor
    * add new subpage with $-plugin usage
    * check rendered text
    """

    def run(self):
        self.performLoginAsAdmin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "dollar_page_" + random_crap.randomText(6)
        inpMenuTitle = "dollar_title_" + random_crap.randomText(6)
        inpPageHeader = "dollar_header_" + random_crap.randomText(6)
        inpAlias = "dollar/plugin/page/" + random_crap.randomText(6)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        #if defaultPageType != "content":
            #self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pluginParam = u'complete-bullshit"\\/&'
        crap1 = random_crap.randomCrap(3)
        crap2 = random_crap.randomCrap(3)
        
        pageText = crap1 + " " + u'${phone:' + slashify(pluginParam) + '}' + " " + crap2
        print "Generated page text: '" + pageText + "'"

        pageText = self.fillAceEditorElement(pageText)
        print "After ins page text: '" + pageText + "'"
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()
        
        expectedText = u"{c1} {dp} {c2}".format(c1=crap1, dp=pluginParam, c2=crap2)
        self.assertElementTextById("content-text", expectedText, "page text does not match expected text. ")

