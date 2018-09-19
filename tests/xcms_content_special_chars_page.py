#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsContentSpecialCharsPage(xtest_common.XcmsTest):
    """
    This test checks content editing - add page with special characters.
    It does following steps:
    * login as root user (in future - site editor)
    * add new subpage with special characters
    * preview page
    * save page
    * load page and test content
    """

    def run(self):
        self.ensure_logged_off()

        self.perform_login_as_editor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "spec_char_page_" + random_crap.random_text(8)
        inpMenuTitle = "spec_menu_title_" + random_crap.random_text(8)
        inpPageHeader = "spec_page_header_" + random_crap.random_text(8)
        inpAlias = "spec/char/page/alias/" + random_crap.random_text(8)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = "&amp;&lt;'"

        pageText = self.fillAceEditorElement(pageText)
        self.clickElementById("preview-submit")
        previewElement = "content-text-preview"
        pageRealText = "&<'"
        self.assertElementTextById(previewElement, pageRealText, "preview text does not match entered page text. ")

        self.clickElementById("commit-submit")

        self.gotoCloseEditor()

        self.getElementById("cabinet")

        # click on menu.
        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(self.m_parentPage, attribute=self.CONTENT)
        self.logAdd("Clicking on new page menu item. ")
        self.gotoUrlByLinkText(inpMenuTitle, attribute=self.CONTENT)

        self.assertElementTextById("content-text", pageRealText, "rendered page text does not match expacted text. ")
        self.gotoEditPageInPlace()

        self.assertAceEditorElementText(pageText, "page text after reopening editor does not match entered HTML text. ")
