#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsUnitTests(SeleniumTest):
	"""
	This test runs unittests and checks if all are passed OK.
	"""
	def run(self):
		self.gotoPage("/unittest.php")
		self.assertSourceTextPresent(u"UNIT TESTS PASSED OK");
		
    