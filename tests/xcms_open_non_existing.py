#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsOpenNonExisting(SeleniumTest):
	"""
	This test checks '404 page' handling in XCMS functional
	Steps:
	* Navigate to non-existing page
	* Check if special page appeared
	* Go to home site url on 404 page
	"""
	def run(self):
		self.setAutoPhpErrorChecking(True)
		
		xtest_common.assertNoInstallerPage(self)
		
		self.gotoPage("/qqq");
		self.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
		homeHref = self.getUrlByLinkText(u"этой ссылке")
		print "Home reference on 404 page: ", homeHref
		self.gotoSite(homeHref)

