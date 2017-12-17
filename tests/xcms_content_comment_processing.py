#!/usr/bin/python
# -*- coding: utf8 -*-

import xpage
import xtest_common


class XcmsContentCommentProcessing(xtest_common.XcmsTest):

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        page = xpage.Page(self)
        page.input(
            page_dir="test_page",
            menu_title="menu_title",
            header="page_header",
            alias="new/page/alias/",
            random=True,
        )

        # edit page - click on menu
        self.gotoUrlByLinkText(page.menu_title)

        page_text = "<?php\n/**\n* qqq\n*\n**/\n?>"
        page_text = self.fillAceEditorElement(page_text)
        self.clickElementById("commit-submit")

        self.performLogoutFromAdminPanel()

        self.gotoUrlByLinkText(page.menu_title, attribute=self.CONTENT)
        self.assertPhpErrors()
