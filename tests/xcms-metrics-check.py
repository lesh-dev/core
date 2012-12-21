#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsMetricsCheck(SeleniumTest):
	"""
	This test checks if metrics counter successfully wiped off from test website.
	"""
	def run(self):
		self.gotoPage("/")
		self.assertSourceTextNotPresent("Metrika");
		
# def main():
selenium_test.RunTest(XcmsMetricsCheck())
    