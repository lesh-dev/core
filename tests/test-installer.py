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
		self.gotoRoot()
		self.assertSourceTextPresent(["XCMS installer", u"Установка XCMS"])
		# very meaningful name...
		self.clickElementByName("submit_variables")
		self.assertSourceTextPresent(u"Установка завершена!")
		self.gotoUrlByLinkText(u"Перейти к сайту")
		
	
# def main():
selenium_test.RunTest(TestInstaller())
    