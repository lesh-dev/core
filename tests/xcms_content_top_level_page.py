#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap


class XcmsContentTopLevelPage(xtest_common.XcmsTest):
    """
    This test checks top-level page add checbox.
    It does following steps:
    * login as root user (in future - site editor)
    * add new top-level page
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.gotoCreatePage()

        inpPageDir = "topLevelPage_" + random_crap.random_text(6);
        inpMenuTitle = "topMenuTitle_" + random_crap.random_text(6);
        inpPageHeader = "topPageHeader_" + random_crap.random_text(6);
        inpAlias = "top/level/page/" + random_crap.random_text(6);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.clickElementById("global-checkbox")

        defaultPageType = self.getOptionValueById("create-pagetype-selector")
        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = random_crap.randomCrap(6)
        self.logAdd("Generated page text: '" + pageText + "'")

        pageText = self.fillAceEditorElement(pageText)
        self.logAdd("Page text after edit: '" + pageText + "'")
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()

        # click on some other menu to change active menu item

        self.logAdd("Clicking on some other menu item. ")
        self.gotoUrlByLinkText(self.get_contacts_link_name())

        self.logAdd("Clicking on new top-level page menu item, it should be visible")
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertElementTextById("content-text", pageText, "page text does not match entered text. ")
        self.assertElementTextById("content-header", inpPageHeader, "page header does not match entered header. ")

        if inpMenuTitle not in self.getPageTitle():
            self.failTest("Menu title text does not appear in page title after going to the page by site menu. ")

