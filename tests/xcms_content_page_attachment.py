#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap

import datetime


def timestamp():
    return datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")


def htmlParagraph(x):
    return "<p>" + x + "</p>"


def linesToHtml(lineArray):
    return "\n".join([htmlParagraph(x) for x in lineArray])


class XcmsContentPageAttachment(xtest_common.XcmsTest):
    """
        Проверяет, что вложения на страницу загружаются корректно
    """

    def run(self):
        self.ensure_logged_off()
        self.perform_login_as_admin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "test_page_" + random_crap.random_text(8)
        inpMenuTitle = "menu_title_" + random_crap.random_text(8)
        inpPageHeader = "page_header_" + random_crap.random_text(8)
        inpAlias = "new/page/alias/" + random_crap.random_text(8)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.m_pageAlias = inpAlias

        defaultPageType = self.getOptionValueById("create-pagetype-selector")

        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")

        # self.logAdd("Opening editor again after redirection. ")
        # self.gotoEditPageInPlace()

        self.m_menuTitle = inpMenuTitle
        self.m_pageHeader = inpPageHeader

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        self.gotoUrlByLinkText(u"Файлы")

        inpFileName = "SomeNameQQQ" + random_crap.random_text(8)
        inpFileName = self.fillElementById("attach_target-input", inpFileName)

        self.clickElementById("upload_attach-submit")

        self.assertPhpErrors()

        self.assertBodyTextPresent("No file selected")
