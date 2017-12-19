#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import user
import xpage


class XcmsContentAuthOnlyPage(xtest_common.XcmsTest):
    """
    This test checks auth-only page add checbox.
    It does following steps:
    * login as root user (in future - site editor)
    * add new auth-only page
    * log out
    * check menu
    * goto page by alias (should not work)
    * login as normal user
    * check menu
    * check alias
    * check page content
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsEditor()
        self.gotoAdminPanel()

        parent_page = u"Главная"

        self.gotoUrlByLinkText(parent_page)

        self.gotoCreatePage()
        page = xpage.Page(self)
        page.input(
            page_dir="authPage",
            menu_title="authMenuTitle",
            header="authPageHeader",
            alias="authorized/only/page/",
            random=True,
            permissions=["view_#all", "view_#registered"],
        )

        # edit page - click on menu
        self.gotoUrlByLinkText(page.menu_title)

        page_text = u"Текст Только Для Авторизованных " + random_crap.randomCrap(6)
        page_text = self.fillAceEditorElement(page_text)
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()
        self.performLogout()

        # click on some other menu to change active menu item
        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(parent_page, attribute=self.CONTENT)

        self.logAdd("Checking new page menu item, it should NOT be visible")
        self.assertUrlNotPresent(page.menu_title)
        self.logAdd("Alias should NOT work too, we should see access denied page")
        self.gotoPage("/" + page.alias)

        self.logAdd("We should NOT see page text at all")
        self.assertSourceTextNotPresent(page_text, "we should not see page text without authorization. ")
        self.assertSourceTextNotPresent(page.header, "we should not see page header without authorization. ")
        self.assertSourceTextPresent(self.STOP_PHRASES, "we should see auth page")

        inp_login = "AuthPageUser"
        inp_name = u"Убер Уполномоченный "

        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            name=inp_name,
            random=True,
        )

        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login as auth-page-test user. ")

        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(parent_page, attribute=self.CONTENT)

        self.logAdd("Checking new page menu item, it should be visible")
        self.gotoUrlByLinkText(page.menu_title, attribute=self.CONTENT)

        self.assertElementTextById(
            "content-text", page_text, "menu check: page text does not match entered text (under auth). "
        )
        self.assert_page_header(page.header)

        self.logAdd("Clicking on some other menu item. ")
        self.goto_contacts()

        self.logAdd("Alias should work now, and we should NOT see access denied page")
        self.gotoPage("/" + page.alias)

        self.assertElementTextById(
            "content-text", page_text, "alias check: page text does not match entered text (under auth). "
        )
        self.assert_page_header(
            page.header,
            reason="Alias check: page header does not match entered header (under auth). "
        )

        self.assertSourceTextNotPresent(self.STOP_PHRASES)
