#!/usr/bin/python
# -*- coding: utf8 -*-

import xpage
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
        self.ensure_logged_off()
        self.perform_login_as_editor()
        self.gotoAdminPanel()

        self.parent_page = u"Главная"

        self.gotoUrlByLinkText(self.parent_page)
        self.gotoCreatePage()

        page = xpage.Page(self)
        page.input(
            page_dir="phoenix_",
            menu_title="phoenix_menu_title_",
            header="phoenix_header_",
            alias="removed/phoenix/alias/",
            random=True,
        )

        # edit page - click on menu
        self.gotoUrlByLinkText(page.menu_title)
        pageText = random_crap.randomCrap(10)
        pageText = self.fillAceEditorElement(pageText)
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()
        self.gotoAdminPanel()

        self.gotoUrlByLinkText(self.parent_page)
        self.gotoUrlByLinkText(page.menu_title)

        self.gotoRemovePage()
        self.assertBodyTextPresent(u"Удаление страницы")
        self.clickElementById("delete_page-submit")

        self.gotoCloseEditor()
        self.gotoUrlByLinkText(self.parent_page, attribute=self.CONTENT)
        if self.get_url_by_link_data(page.menu_title, attribute=self.CONTENT, fail=False) is not None:
            self.failTest("Page should be removed")

        # create same page again
        self.gotoAdminPanel()
        self.gotoUrlByLinkText(self.parent_page)
        self.gotoCreatePage()

        page.input(
            page_dir=page.page_dir,
            menu_title=page.menu_title,
            header=page.header,
            alias=page.alias,
        )
        self.gotoUrlByLinkText(page.menu_title)

        newPageText = random_crap.randomCrap(10)
        newPageText = self.fillAceEditorElement(pageText)
        self.clickElementById("commit-submit")
        self.gotoCloseEditor()

        self.gotoUrlByLinkText(self.parent_page, attribute=self.CONTENT)
        self.gotoUrlByLinkText(page.menu_title, attribute=self.CONTENT)

        self.assertElementTextById(
            "content-text", newPageText,
            "new page text should appear after page reincarnation. "
        )

        self.goto_alias(page.alias)
