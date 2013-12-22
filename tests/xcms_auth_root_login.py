#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
from xtest_config import XcmsTestConfig

class XcmsAuthRootLogin(xtest_common.XcmsTestWithConfig):
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
		
		self.performLoginAsAdmin()
		self.gotoAdminPanel()
		
		self.assertBodyTextPresent(self.getUserListLinkName())
		self.assertBodyTextPresent(u"Очистить кэш")
	
