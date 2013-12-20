#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsVersionCheck(xtest_common.XcmsTest):
    """
    This test checks if version is displayed on main page and in admin panel.
    """
    def run(self):
        
        self.gotoRoot()

        # frontend 
        feVerXpath = "//span[@class='site-version']"
        self.assertTextPresent(feVerXpath, "rev.");
        siteVersion = self.getElementText(feVerXpath);
        print "XCMS version: ", siteVersion
        
        # master-2.1 rev. 848
        versionRegexp = "[\w\d_]+\-[\d\.]+ rev\. [\d]+"
        m = re.search(versionRegexp, siteVersion)
        if not m:
            self.failTest("Site version does not match expected regexp. ");
        
        xtest_common.performLoginAsAdmin(self, self.getAdminLogin(), self.getAdminPass())
        xtest_common.gotoAdminPanel(self)
        
        # backend
        beVerXpath = "//pre[@class='site-info']"
        self.assertTextPresent(beVerXpath, "rev.");
        cpVersion = self.getElementText(beVerXpath);
        print "XCMS version in CP: ", cpVersion
        m = re.search(versionRegexp, cpVersion)
        if not m:
            self.failTest("Site version in admin CP does not match expected regexp. ");
    