#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsUnitTests(SeleniumTest):
	"""
	This test runs unittests and checks if all are passed OK.
	"""
	def run(self):
		self.gotoPage("/unittest.php")
		self.assertSourceTextPresent(u"UNIT TESTS PASSED OK");
		
# def main():
selenium_test.RunTest(XcmsUnitTests())
    