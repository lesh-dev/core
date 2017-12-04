#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import xpage


class XcmsContentPageOrder(xtest_common.XcmsTest):
    """
    This test checks page order management
    """

    def pre_create_page(self, parent_page):
        self.checkScreenIsAdmin()
        self.gotoUrlByLinkText(parent_page)
        self.gotoCreatePage()

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsEditor()
        self.gotoAdminPanel()

        parent_page = u"Главная"

        self.pre_create_page(parent_page)
        page1 = xpage.Page(self)
        page1.input(
            page_dir="pageOrderTest1",
            menu_title="pageOrderTestMenu1",
            header="hiddenPageHeader1",
            alias="page/order/test1",
            random=True,
        )

        self.pre_create_page(parent_page)
        page2 = xpage.Page(self)
        page2.input(
            page_dir="pageOrderTest2",
            menu_title="pageOrderTestMenu2",
            header="hiddenPageHeader2",
            alias="page/order/test2",
            random=True,
        )

        self.pre_create_page(parent_page)
        page3 = xpage.Page(self)
        page3.input(
            page_dir="pageOrderTest3",
            menu_title="pageOrderTestMenu3",
            header="hiddenPageHeader3",
            alias="page/order/test3",
            random=True,
        )

        # edit page - click on menu
        self.gotoUrlByLinkText(page1.menu_title)
        self.clickElementById("edit-menu")

        order1 = "20"
        order1 = self.fillElementById("menu-order-input", order1)
        self.clickElementByName("change-menu")

        # edit page - click on menu
        self.gotoUrlByLinkText(page2.menu_title)
        self.clickElementById("edit-menu")

        order2 = "30"
        order2 = self.fillElementById("menu-order-input", order2)
        self.clickElementByName("change-menu")

        # edit page - click on menu
        self.gotoUrlByLinkText(page3.menu_title)
        self.clickElementById("edit-menu")

        order3 = "10"
        order3 = self.fillElementById("menu-order-input", order3)
        self.clickElementByName("change-menu")

        self.closeAdminPanel()
        self.gotoUrlByLinkText(parent_page, attribute=self.CONTENT)

        content = self.getPageSource()

        try:
            index1 = content.index(page1.menu_title)
            index2 = content.index(page2.menu_title)
            index3 = content.index(page3.menu_title)
            if index3 < index1 < index2:
                pass
            else:
                self.failTest("Page order does not match expected. ")
        except ValueError:
            self.failTest("One of page menu titles could not be found in page source. ")
