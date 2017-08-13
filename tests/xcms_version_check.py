#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import xtest_common


class XcmsVersionCheck(xtest_common.XcmsTest):
    """
    This test checks if version is displayed on main page and in admin panel.
    """
    def run(self):
        self.ensure_logged_off()
        self.gotoRoot()

        # frontend
        version_xpath = "//span[@class='site-version']"
        self.assertTextPresent(version_xpath, "master-r")
        site_version = self.getElementText(version_xpath)
        print "XCMS version: ", site_version

        # 2.15.8-master-r3408-5e0a-27e1-local
        # 2.15.8-master-r3408

        version_regexp = "\d+\.\d+\.\d+-master-r\d+"

        m = re.search(version_regexp, site_version)
        if not m:
            self.failTest("Site version does not match expected regexp. ")

        self.performLoginAsAdmin()
        self.logAdd("before admin panel")
        self.gotoAdminPanel()

        # backend
        backend_version_xpath = "//pre[@class='site-info']"
        self.assertTextPresent(backend_version_xpath, "rev.")
        control_panel_version = self.getElementText(backend_version_xpath)
        print "XCMS version in Control Panel: ", control_panel_version

        m = re.search(version_regexp, control_panel_version)
        if not m:
            self.failTest("Site version in admin CP does not match expected regexp. ")
