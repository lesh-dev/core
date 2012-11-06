#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsOverallOpenPages(SeleniumTest):
	"""
	This test checks '404 page' handling in XCMS functional
	Steps:
	* Navigate to non-existing page
	* Check if special page appeared
	* Go to home site url on 404 page
	"""
	def run(self):
		self.setAutoPhpErrorChecking(True)
		self.gotoPage("/qqq");
		self.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
		homeHref = self.getUrlByLinkText(u"этой ссылке")
		print "Home reference on 404 page: ", homeHref
		self.gotoSite(homeHref)

# def main():	
selenium_test.RunTest(XcmsOverallOpenPages())