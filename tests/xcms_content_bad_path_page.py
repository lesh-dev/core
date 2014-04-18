#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsContentBadPathPage(xtest_common.XcmsTest):
    """
    This test checks content editing - try add page bad physical path
    It does following steps:
    * login as site editor
    * add new subpage with bad characters in path
    * checks that page was not added
    """

    def run(self):

        self.performLoginAsEditor()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "../../hacked_page_" + random_crap.randomText(8);
        inpMenuTitle = "hacked_menu_title_" + random_crap.randomText(8);
        inpPageHeader = "hacked_header_" + random_crap.randomText(8);
        inpAlias = "hacked/page/alias/" + random_crap.randomText(8);

        inpPageDir = self.fillElementById("create-name-input", inpPageDir);
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle);
        inpPageHeader = self.fillElementById("header-input", inpPageHeader);
        inpAlias = self.fillElementById("alias-input", inpAlias);

        self.clickElementById("create-page-submit")
        self.assertBodyTextPresent(u"Недопустимый физический путь страницы")

        # ensure that page was not actually created. 
        self.assertUrlNotPresent(inpMenuTitle)

