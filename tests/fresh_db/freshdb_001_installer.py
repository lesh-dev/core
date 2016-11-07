#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common


class FreshDbInstaller(xtest_common.XcmsTestWithConfig):
    """
    This test checks XCMS installator with fresh database.
    It does following steps:
    * navigates to setup form
    * submits form with default values except db name
    * checks if 'installation complete' message appeared
    * checks if 'Creating fresh database' message appeared
    """

    def run(self):
        self.gotoRoot()

        self.assertSourceTextPresent(["XCMS installer", u"Установка XCMS"], "Here should be installer page. ")
        self.fillElementById("xsm_db_name", "ank/freshdb.sqlite3")
        self.clickElementByName("submit_variables")
        self.assertSourceTextPresent(u"Установка завершена!")
        self.assertSourceTextPresent("Creating fresh database")
        self.gotoUrlByLinkText(u"Перейти к сайту")

        self.setTestNotifications()
        self.checkTestNotifications()

    def check_doc_type(self):
        self.logAdd("DOCTYPE checking disabled for installer test. ", "warning")
