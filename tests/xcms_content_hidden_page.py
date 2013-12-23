#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsContentHiddenPage(xtest_common.XcmsTest):
    """
    This test checks hidden page add checbox.
    It does following steps:
    * login as root user (in future - site editor)
    * add new hidden page
    * log out
    * check menu
    * goto page by alias
    """

    def run(self):

        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"
        self.gotoUrlByLinkText(self.m_parentPage)

        self.gotoCreatePage()

        inpPageDir = "hiddenPage_" + random_crap.randomText(6);
        inpMenuTitle = "hiddenMenuTitle_" + random_crap.randomText(6);
        inpPageHeader = "hiddenPageHeader_" + random_crap.randomText(6);
        inpAlias = "hidden/secret/page/" + random_crap.randomText(6);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.clickElementById("menu-hidden-checkbox")

        defaultPageType = self.getOptionValueById("create-pagetype-selector")
        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        #TODO: wait for fixing of bug with automatic alias rebuildAliases
        self.logAdd("Rebuilding aliases for first time to w/a bug ")
        self.gotoRebuildAliases()
        #self.wait(2)

        # edit page - click on menu
        self.gotoUrlByLinkText("H" + inpMenuTitle)

        pageText = u"Секретный Скрытый Текст" + random_crap.randomCrap(6)
        pageText = self.fillElementById("edit-text", pageText)
        self.clickElementById("edit-submit-top")

        self.gotoCloseEditor()
        self.performLogout()

        # click on some other menu to change active menu item

        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(self.m_parentPage)

        self.logAdd("Checking new page menu item, it should NOT be visible")
        self.assertUrlNotPresent(inpMenuTitle)
        self.logAdd("Alias should work fine")
        self.gotoPage("/" + inpAlias)

        self.logAdd("We should see page text")
        self.assertElementTextById("content-text", pageText, "page text does not match entered text. ")
        self.assertElementTextById("content-header", inpPageHeader, "page header does not match entered header. ")

        if inpMenuTitle not in self.getPageTitle():
            self.failTest("Menu title text does not appear in page title after going to the page by site menu. ")

