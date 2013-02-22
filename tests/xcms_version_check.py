#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsVersionCheck(SeleniumTest):
	"""
	This test checks if version is displayed on main page and in admin panel.
	"""
	def run(self):
		
		xtest_common.assertNoInstallerPage(self)

		self.gotoRoot()

		# frontend 
		feVerXpath = "//span[@class='site-version']"
		self.assertTextPresent(feVerXpath, "rev. ");
		siteVersion = self.getElementContent(feVerXpath);
		print "XCMS version: ", siteVersion
		
		# master-2.1 rev. 848
		versionRegexp = "[\w\d_]+\-[\d\.]+ rev\. [\d]+"
		m = re.search(versionRegexp, siteVersion)
		if not m:
			raise selenium_test.TestError("Site version does not match expected regexp. ");
		
		conf = XcmsTestConfig()
		
		xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
		
		xtest_common.gotoAdminPanel(self)
		
		# backend
		beVerXpath = "//pre[@class='site-info']"
		self.assertTextPresent(beVerXpath, "rev. ");
		cpVersion = self.getElementContent(beVerXpath);
		print "XCMS version in CP: ", cpVersion
		m = re.search(versionRegexp, cpVersion)
		if not m:
			raise selenium_test.TestError("Site version in admin CP does not match expected regexp. ");
    