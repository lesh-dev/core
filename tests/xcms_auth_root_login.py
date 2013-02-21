#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthRootLogin(SeleniumTest):
	"""
	This test checks root login functional.
	It does following steps:
	* navigates to main page
	* clicks on Authorization link
	* enters root's credentials
	* checks if admin CP appears
	"""
	
	def run(self):
		self.setAutoPhpErrorChecking(True)
		self.maximizeWindow()
		
		conf = XcmsTestConfig()
		
		xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
		
		self.gotoUrlByLinkText(u"Админка")
		
		self.assertBodyTextPresent(u"Пользователи")
		self.assertBodyTextPresent(u"Очистить кэш")
	