#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsMetricsCheck(xtest_common.XcmsTest):
	"""
	This test checks if metrics counter successfully wiped off from test website.
	"""
	def run(self):

		self.setAutoPhpErrorChecking(True)
		
		xtest_common.assertNoInstallerPage(self)
		
		self.gotoRoot();
		self.assertSourceTextNotPresent("Metrika");
		
    