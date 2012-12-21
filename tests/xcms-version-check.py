#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsVersionCheck(SeleniumTest):
	"""
	This test checks if version is displayed on main page and in admin panel.
	"""
	def run(self):
		self.gotoPage("/")
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
		
		tests_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
		
		self.gotoUrlByLinkText("Админка")
		
		
		beVerXpath = "//pre[@class='site-info']"
		self.assertTextPresent(beVerXpath, "rev. ");
		cpVersion = self.getElementContent(beVerXpath);
		print "XCMS version in CP: ", cpVersion
		m = re.search(versionRegexp, cpVersion)
		if not m:
			raise selenium_test.TestError("Site version in admin CP does not match expected regexp. ");
		
# def main():
selenium_test.RunTest(XcmsVersionCheck())
    