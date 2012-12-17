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
		self.assertTextPresent("//span[@class='site-version']", "rev. ");
		siteVersion = self.getElementContent("//span[@class='site-version']");
		print "XCMS version: ", siteVersion
		m = re.search("[\w\d\-_\.]+[\d\.]+ rev\. [\d]+", siteVersion)
		if not m:
			raise selenium_test.TestError("Site version does not patch expected regexp. ");
		
# def main():
selenium_test.RunTest(XcmsVersionCheck())
    