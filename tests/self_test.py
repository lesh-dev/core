#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class SelfTest(SeleniumTest):
	"""
	This test checks SeleniumTest class.
	"""
			
	def run(self):
		self.setAutoPhpErrorChecking(True)
		self.gotoRoot()
		
		conf = XcmsTestConfig()

		xtest_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())

		self.gotoUrlByLinkText(u"Анкеты")
		self.gotoUrlByLinkText(u"TESTЧаПаев626df Василий72f")
		
		self.gotoIndexedUrlByLinkText(u"Правка", 0)		
		

