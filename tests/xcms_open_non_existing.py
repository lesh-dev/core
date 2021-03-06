#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common


class XcmsOpenNonExisting(xtest_common.XcmsBaseTest):
    """
    This test checks '404 page' handling in XCMS functional
    Steps:
    * Navigate to non-existing page
    * Check if special page appeared
    * Go to home site url on 404 page
    """
    def run(self):
        self.setAutoPhpErrorChecking(True)

        self.assert_no_installer_page()

        self.set404Checking(False)

        self.gotoPage("/qqq")
        self.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
        home_href = self.get_url_by_link_data(u"этой ссылке")
        print "Home reference on 404 page: ", home_href
        self.gotoSite(home_href)
