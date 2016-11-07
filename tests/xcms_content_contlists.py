#!/usr/bin/python
# -*- coding: utf8 -*-

import datetime

import xtest_common
import random_crap


def slashify(line):
    return "".join([x * 2 if x == "\\" else x for x in line])


class XcmsContentContlist(xtest_common.XcmsTest):
    """
    This test checks cont-lists functionality.
    Steps:
    * login as site editor
    * add new subpage with type 'cont-list', fills one block
    * check rendered text
    """

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsAdmin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        inpPageDir = "contlist_dir_" + random_crap.random_text(5)
        inpMenuTitle = "contlist_mt_" + random_crap.random_text(5)
        inpPageHeader = "contlist_ph_" + random_crap.random_text(5)
        inpAlias = "cont/list/page" + random_crap.random_text(5)

        inpPageDir = self.fillElementById("create-name-input", inpPageDir)
        inpMenuTitle = self.fillElementById("menu-title-input", inpMenuTitle)
        inpPageHeader = self.fillElementById("header-input", inpPageHeader)
        inpAlias = self.fillElementById("alias-input", inpAlias)

        self.m_pageAlias = inpAlias

        self.setOptionValueByIdAndValue("create-pagetype-selector", "contlist")

        pageDate = datetime.datetime.now()

        self.clickElementById("create-page-submit")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle)

        blockTitle = "block_title_" + random_crap.random_text(5)
        blockContent = random_crap.randomCrap(10, crapOptions=["multiline"])

        blockTitle = self.fillElementById("header-input", blockTitle)
        blockContent = self.fillElementById("content", blockContent)

        self.clickElementById("contlist-create-submit")
        self.wait(3)

        # we are still on admin page.
        # get generated alias.

        blockAlias = self.getElementTextById("edit-alias")
        self.logAdd("Alias: {0}".format(blockAlias))

        self.gotoCloseEditor()
        self.gotoUrlByLinkText(inpMenuTitle)

        dateStr = pageDate.strftime("%d.%m.%Y")
        self.assertElementSubTextById("content-text", dateStr, "Contlist timestamp not found")
        self.assertElementSubTextById("content-text", blockTitle, "Block title not found in rendered cont-list. ")
        blockContentForCheck = blockContent.replace("\n", " ").replace("  ", " ")
        print self.getElementTextById("content-text")
        print blockContentForCheck
        self.assertElementSubTextById("content-text", blockContentForCheck, "Block content not found in rendered cont-list. ")

        # check alias
        # expected: displayed one block with title
        self.goto_alias(blockAlias)
        self.assertElementSubTextById("content-header", blockTitle, "Block title not found after clicking by alias. ")
        self.assertElementSubTextById("content-text", blockContentForCheck, "Block content not found after clicking by alias. ")
