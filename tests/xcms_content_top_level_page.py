#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import xpage


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
        page = xpage.Page(self)
        page.input(
            page_dir="topLevelPage",
            menu_title="topMenuTitle",
            header="topPageHeader",
            alias="top/level/page",
            global_page=True,
        )

        # edit page - click on menu
        self.gotoUrlByLinkText(page.menu_title)

        page_text = random_crap.randomCrap(6)
        self.logAdd("Generated page text: '" + page_text + "'")

        page_text = self.fillAceEditorElement(page_text)
        self.logAdd("Page text after edit: '" + page_text + "'")
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()

        # click on some other menu to change active menu item
        self.goto_contacts()
        self.logAdd("Clicking on some other menu item. ")

        self.logAdd("Clicking on new top-level page menu item, it should be visible")
        self.gotoUrlByLinkText(page.menu_title, attribute=self.CONTENT)

        self.assertElementTextById("content-text", page_text, "page text does not match entered text. ")
        self.assert_page_header(page.header)
