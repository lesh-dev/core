#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

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
		
		xtest_common.assertNoInstallerPage(self)
		
		self.gotoPage("/qqq");
		self.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
		homeHref = self.getUrlByLinkText(u"этой ссылке")
		print "Home reference on 404 page: ", homeHref
		self.gotoSite(homeHref)

