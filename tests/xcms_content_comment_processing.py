#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsContentCommentProcessing(xtest_common.XcmsTest):

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "test_page_" + random_crap.randomText(8)
        inpMenuTitle = "menu_title_" + random_crap.randomText(8)
        inpPageHeader = "page_header_" + random_crap.randomText(8)
        inpAlias = "new/page/alias/" + random_crap.randomText(8)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        # self.logAdd("Opening editor again after redirection. ")
        # self.gotoEditPageInPlace()

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = "<?php\n/**\n* qqq\n*\n**/\n?>"
        # print "Generated page text: '" + pageText + "'"

        pageText = self.fillAceEditorElement(pageText)
        # print "After ins page text: '" + pageText + "'"
        self.clickElementById("commit-submit")

        self.performLogoutFromAdminPanel()

        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertPhpErrors()
