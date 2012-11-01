#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class TestInstaller(SeleniumTest):
	"""
	This test checks XCMS installator.
	It does following steps:
	* navigates to setup form
	* submits form with default values
	* checks if 'installation complete' message appeared
	"""
	
	def run(self):
		test.gotoRoot()
		self.assertTextPresent("XCMS installer")
		# very meaningful name...
		self.clickElementByName("submit_variables")
		self.assertTextPresent(u"Установка завершена!")
	
# def main():
selenium_test.RunTest(TestInstaller())
    