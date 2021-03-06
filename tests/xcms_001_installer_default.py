#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common


class XcmsInstallerDefault(xtest_common.XcmsTestWithConfig):
    """
    This test checks XCMS installator.
    It does following steps:
    * navigates to setup form
    * submits form with default values
    * checks if 'installation complete' message appeared
    """

    def run(self):
        self.goto_root()

        self.assertSourceTextPresent(["XCMS installer", u"Установка XCMS"], "Here should be installer page. ")
        self.clickElementByName("submit_variables")
        self.assertSourceTextPresent(u"Установка завершена!")
        self.gotoUrlByLinkText(u"Перейти к сайту")

        self.setTestNotifications()
        self.checkTestNotifications()

    def check_doc_type(self):
        self.logAdd("DOCTYPE checking disabled for installer test. ", "warning")
