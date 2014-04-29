#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

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

        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "spec_char_page_" + random_crap.randomText(8);
        inpMenuTitle = "spec_menu_title_" + random_crap.randomText(8);
        inpPageHeader = "spec_page_header_" + random_crap.randomText(8);
        inpAlias = "spec/char/page/alias/" + random_crap.randomText(8);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = "&amp;&lt;"

        pageText = self.fillElementById("edit-text", pageText)
        self.clickElementById("edit-preview-top")
        previewElement = "content-text-preview"
        pageRealText = "&<";
        self.assertElementTextById(previewElement, pageRealText, "preview text does not match entered page text. ")

        self.clickElementById("edit-submit-top")

        self.gotoCloseEditor()

        self.assertUrlPresent(u"Личный кабинет")
        # click on menu.

        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(self.m_parentPage)
        self.logAdd("Clicking on new page menu item. ")
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertElementTextById("content-text", pageRealText, "rendered page text does not match expacted text. ")
        self.gotoEditPageInPlace()

        self.assertElementTextById("edit-text", pageText, "page text after reopening editor does not match entered HTML text. ")
