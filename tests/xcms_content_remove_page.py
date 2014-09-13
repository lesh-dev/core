#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap

class XcmsContentRemovePage(xtest_common.XcmsTest):
    """
    This test checks content editing - page remove and re-create functional.
    Steps:
    * login as site editor
    * add new subpage
    * remove this page
    * create page with same parameters to test ticket #781
    """

    def run(self):

        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "phoenix_" + random_crap.randomText(8);
        inpMenuTitle = "phoenix_menu_title_" + random_crap.randomText(8);
        inpPageHeader = "phoenix_header_" + random_crap.randomText(8);
        inpAlias = "removed/phoenix/alias/" + random_crap.randomText(8);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.clickElementById("create-page-submit")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = random_crap.randomCrap(10)
        pageText = self.fillAceEditorElement(pageText)
        self.clickElementById("edit-submit-top")

        self.gotoCloseEditor()
        self.gotoAdminPanel()

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoUrlByLinkText(inpMenuTitle)
        
        self.gotoRemovePage()
        self.assertBodyTextPresent(u"Удаление страницы")
        self.clickElementById("delete_page-button")
        
        self.gotoCloseEditor()
        self.gotoUrlByLinkText(self.m_parentPage)
        self.assertUrlNotPresent(inpMenuTitle, "page should be removed")

        # create same page again
        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()
        
        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.clickElementById("create-page-submit")
        
        self.gotoUrlByLinkText(inpMenuTitle)

        newPageText = random_crap.randomCrap(10)
        newPageText = self.fillAceEditorElement(pageText)
        self.clickElementById("edit-submit-top")
        self.gotoCloseEditor()
        
        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoUrlByLinkText(inpMenuTitle)
        
        self.assertElementTextById("content-text", newPageText, "new page text should appear after page reincarnation. ")

