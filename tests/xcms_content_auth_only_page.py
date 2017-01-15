#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import user


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

        parentPage = u"Главная"

        self.gotoUrlByLinkText(parentPage)

        self.gotoCreatePage()

        inpPageDir = "authPage_" + random_crap.random_text(6)
        inpMenuTitle = "authMenuTitle_" + random_crap.random_text(6)
        pageHeader = "authPageHeader_" + random_crap.random_text(6)
        inpAlias = "authorized/only/page/" + random_crap.random_text(6)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        pageHeader = self.fillElementById("header-input", pageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.assertCheckboxValueById("view_#all-checkbox", True)
        self.assertCheckboxValueById("view_#registered-checkbox", False)

        self.clickElementById("view_#all-checkbox")
        self.clickElementById("view_#registered-checkbox")

        defaultPageType = self.getOptionValueById("create-pagetype-selector")
        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        pageText = u"Текст Только Для Авторизованных " + random_crap.randomCrap(6)
        pageText = self.fillAceEditorElement(pageText)
        self.clickElementById("commit-submit")

        self.gotoCloseEditor()
        self.performLogout()

        # click on some other menu to change active menu item

        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(parentPage)

        self.logAdd("Checking new page menu item, it should NOT be visible")
        self.assertUrlNotPresent(inpMenuTitle)
        self.logAdd("Alias should NOT work too, we should see access denied page")
        self.gotoPage("/" + inpAlias)

        self.logAdd("We should NOT see page text at all")
        self.assertSourceTextNotPresent(pageText, "we should not see page text without authorization. ")
        self.assertSourceTextNotPresent(pageHeader, "we should not see page header without authorization. ")

        if inpMenuTitle in self.getPageTitle():
            self.failTest("Menu title text appears in page title after going to the page by site menu without authorization. ")

        self.assertSourceTextPresent([u"Доступ запрещён", "Access denied"], "we should see auth page")

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
        self.gotoUrlByLinkText(parentPage)

        self.logAdd("Checking new page menu item, it should be visible")
        self.gotoUrlByLinkText(inpMenuTitle)

        self.assertElementTextById("content-text", pageText, "menu check: page text does not match entered text (under auth). ")
        self.assertElementTextById("content-header", pageHeader, "menu check: page header does not match entered header (under auth). ")

        if inpMenuTitle not in self.getPageTitle():
            self.failTest("Menu title text does not appear in page title after going to the page by site menu (under auth). ")

        self.logAdd("Clicking on some other menu item. ")
        self.gotoUrlByLinkText(self.getNewsLinkName())

        self.logAdd("Alias should work now, and we should NOT see access denied page")
        self.gotoPage("/" + inpAlias)

        self.assertElementTextById("content-text", pageText, "alias check: page text does not match entered text (under auth). ")
        self.assertElementTextById("content-header", pageHeader, "alias check: page header does not match entered header (under auth). ")

        if inpMenuTitle not in self.getPageTitle():
            self.failTest("Menu title text does not appear in page title after going to the page by site menu (under auth). ")

        self.assertSourceTextNotPresent([u"Доступ запрещён", "Access denied"])
