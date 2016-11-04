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
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "dollar_page_" + random_crap.random_text(6)
        inpMenuTitle = "dollar_title_" + random_crap.random_text(6)
        inpPageHeader = "dollar_header_" + random_crap.random_text(6)
        inpAlias = "dollar/plugin/page/" + random_crap.random_text(6)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        #if defaultPageType != "content":
            #self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.logAdd("Submitting new page")
        self.clickElementById("create-page-submit")

        self.wait(1)

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        plugin_param = u'complete-bullshit"\\/&'
        crap1 = random_crap.randomCrap(3)
        crap2 = random_crap.randomCrap(3)
        
        page_text = crap1 + " " + u'${phone:' + slashify(plugin_param) + '}' + " " + crap2
        print "Generated page text: '" + page_text + "'"

        page_text = self.fillAceEditorElement(page_text)
        print "After ins page text: '" + page_text + "'"
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()
        
        expected_text = u"{c1} {dp} {c2}".format(c1=crap1, dp=plugin_param, c2=crap2)
        self.assertElementTextById("content-text", expected_text, "page text does not match expected text. ")

