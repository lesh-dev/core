#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsContentNestedAliases(xtest_common.XcmsTest):
    """
    This test checks that nested aliases /qqq and /qqq/www work fine
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir1 = "nested_alias1_" + random_crap.random_text(4)
        inpMenuTitle1 = "nested_alias1_" + random_crap.random_text(4)
        inpPageHeader1 = "nested_alias1_" + random_crap.random_text(4)
        inpAlias1 = "nested_alias_" + random_crap.random_text(4) + "/level1"
        inpAlias2 = inpAlias1 + "/level2"

        inpPageDir1 = self.fillElementById("create-name-input", inpPageDir1)
        inpMenuTitle1 = self.fillElementById("menu-title-input", inpMenuTitle1)
        inpPageHeader1 = self.fillElementById("header-input", inpPageHeader1)
        inpAlias1 = self.fillElementById("alias-input", inpAlias1)

        self.clickElementById("create-page-submit")

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir2 = "nested_alias2_" + random_crap.random_text(4)
        inpMenuTitle2 = "nested_alias2_" + random_crap.random_text(4)
        inpPageHeader2 = "nested_alias2_" + random_crap.random_text(4)

        inpPageDir2 = self.fillElementById("create-name-input", inpPageDir2)
        inpMenuTitle2 = self.fillElementById("menu-title-input", inpMenuTitle2)
        inpPageHeader2 = self.fillElementById("header-input", inpPageHeader2)
        inpAlias2 = self.fillElementById("alias-input", inpAlias2)

        self.clickElementById("create-page-submit")

        self.closeAdminPanel()

        self.goto_alias(inpAlias1)
        self.assertSitePageHeader(inpPageHeader1)
        self.goto_alias(inpAlias2)
        self.assertSitePageHeader(inpPageHeader2)
