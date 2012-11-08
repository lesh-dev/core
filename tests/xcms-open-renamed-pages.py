#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsOpenRenamedPages(SeleniumTest):
	"""
	This test checks renamed pages (rewrite rules)
	It does following steps:
	* navigates to all current pages and checks some specific content on each page plus PHP errors.
	"""
	def run(self):
		

# current rename list:
		#index/doctor-1170556276 index/history
		#z024Official/lesh-1311690176 z021Official/lesh-2011-by-serge
		#z024Official/root-1174265356 z021Official/for-parents
		#z024Official z021Official
		#z03Education/Arseniy-1205009664 z03Education/biophys-group
		#z04Science/dimchik-1170608299 z04Science/science-works
		#z04Science/dimchik-1170608594 z04Science/seminar
		#z060JoinUs/anketa-send-fail z024JoinUs/anketa-send-fail
		#z060JoinUs/anketa-send-success z024JoinUs/anketa-send-success
		#z060JoinUs/doctor-1170705932 z024JoinUs/anketa
		#z060JoinUs z024JoinUs
		
		self.setAutoPhpErrorChecking(True)
		self.gotoPage("/")
		
		
# def main():
selenium_test.RunTest(XcmsOpenRenamedPages())
    