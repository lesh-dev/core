#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsMetricsCheck(SeleniumTest):
	"""
	This test checks if metrics counter successfully wiped off from test website.
	"""
	def run(self):

		self.setAutoPhpErrorChecking(True)
		
		xtest_common.assertNoInstallerPage(self)
		
		self.gotoRoot();
		self.assertSourceTextNotPresent("Metrika");
		
    