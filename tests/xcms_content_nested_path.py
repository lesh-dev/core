#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsContentNestedPathPage(xtest_common.XcmsTest):
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
        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "nested/path/page_" + random_crap.random_text(8)
        inpMenuTitle = "nested/path/page_" + random_crap.random_text(8)
        inpPageHeader = "nested/path/page_" + random_crap.random_text(8)
        inpAlias = "nested/path/page/alias" + random_crap.random_text(8)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        self.assertBodyTextPresent(u"Недопустимый физический путь страницы")
        self.closeAdminPanel()
        self.assertPageNotPresent("/" + inpAlias, "Page should not be created due to wrong physical path. ")
