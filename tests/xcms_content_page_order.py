#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsContentPageOrder(xtest_common.XcmsTest):
    """
    This test checks page order management
    """

    def run(self):

        self.performLoginAsEditor()
        self.gotoAdminPanel()
                    
        parentPage = u"Главная"
        
        inpPageDir1 = "pageOrderTest1_" + random_crap.randomText(4)
        inpMenuTitle1 = "pageOrderTestMenu1_" + random_crap.randomText(4)
        inpPageHeader1 = "hiddenPageHeader1_" + random_crap.randomText(4)
        inpAlias1 = "page/order/test1_" + random_crap.randomText(4)
        self.addNewPage(parentPage, inpPageDir1, inpMenuTitle1, inpPageHeader1, inpAlias1)

        inpPageDir2 = "pageOrderTest2_" + random_crap.randomText(4)
        inpMenuTitle2 = "pageOrderTestMenu2_" + random_crap.randomText(4)
        inpPageHeader2 = "hiddenPageHeader2_" + random_crap.randomText(4)
        inpAlias2 = "page/order/test2_" + random_crap.randomText(4)
        self.addNewPage(parentPage, inpPageDir2, inpMenuTitle2, inpPageHeader2, inpAlias2)

        inpPageDir3 = "pageOrderTest3_" + random_crap.randomText(4)
        inpMenuTitle3 = "pageOrderTestMenu3_" + random_crap.randomText(4)
        inpPageHeader3 = "hiddenPageHeader3_" + random_crap.randomText(4)
        inpAlias3 = "page/order/test3_" + random_crap.randomText(4)
        self.addNewPage(parentPage, inpPageDir3, inpMenuTitle3, inpPageHeader3, inpAlias3)
        
        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle1)
        self.clickElementById("edit-menu")

        order1 = "20"
        pageText = self.fillElementById("menu-order-input", order1)
        self.clickElementByName("change-menu")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle2)
        self.clickElementById("edit-menu")

        order2 = "30"
        pageText = self.fillElementById("menu-order-input", order2)
        self.clickElementByName("change-menu")

        # edit page - click on menu
        self.gotoUrlByLinkText(inpMenuTitle3)
        self.clickElementById("edit-menu")

        order3 = "10"
        pageText = self.fillElementById("menu-order-input", order3)
        self.clickElementByName("change-menu")

        self.closeAdminPanel()
        self.gotoUrlByLinkText(parentPage)
        
        content = self.getPageSource()

        try:
            index1 = content.index(inpMenuTitle1)
            index2 = content.index(inpMenuTitle2)
            index3 = content.index(inpMenuTitle3)
            if index3 < index1 < index2:
                pass
            else:
                self.failTest("Page order does not match expected. ")
        except ValueError:
            self.failTest("One of page menu titles could not be found in page source. ")
            

