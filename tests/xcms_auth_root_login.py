#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsAuthRootLogin(xtest_common.XcmsBaseTest):
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
		
		xtest_common.gotoAdminPanel(self)
		
		self.assertBodyTextPresent(u"Пользователи")
		self.assertBodyTextPresent(u"Очистить кэш")
	