#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsDownloadSeparateResources(SeleniumTest):
	"""
	This test checks /lectures folder (check it is not confused be rewrite rules)
	It does following steps:
	* navigates to /lectures folder.
	"""
	def run(self):
		self.gotoPage("/")
		self.gotoPage("/lectures")
		self.gotoPage("/lectures/iext.pdf")
		self.gotoPage("/lectures/iext-by-an.pdf")
		self.gotoPage("/lectures/prak")
		
# def main():
selenium_test.RunTest(XcmsDownloadSeparateResources())
    