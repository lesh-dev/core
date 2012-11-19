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
		self.gotoPage("/")
		self.gotoPage("/?page=index/doctor-1170556276") # index/history
		self.assertBodyTextPresent(u"История")

		self.gotoPage("/?page=z024Official/lesh-1311690176") # lesh2011-by-serge
		self.assertBodyTextPresent(u"МОИ ЛИЧНЫЕ НАБЛЮДЕНИЯ")

		self.gotoPage("/?page=z024Official/root-1174265356") # info/parents
		self.assertBodyTextPresent(u"Родителям школьников")

		self.gotoPage("/?page=z03Education/Arseniy-1205009664") # biophys
		self.assertBodyTextPresent(u"Биофизическая группа открыта для школьников")

		self.gotoPage("/?page=z04Science/dimchik-1170608299") # science works
		self.assertBodyTextPresent(u"возможность выполнения исследовательских работ")

		self.gotoPage("/?page=z04Science/dimchik-1170608594") # science works
		self.assertBodyTextPresent(u"на ЛЭШ работает межотделенческий семинар")

		self.gotoPage("/?page=z060JoinUs/anketa-send-fail")
		self.assertBodyTextPresent(u"По техническим причинам анкета")

		self.gotoPage("/?page=z060JoinUs/anketa-send-success")
		self.assertBodyTextPresent(u"свяжется один из наших координаторов")

		self.gotoPage("/?page=z060JoinUs/doctor-1170705932") # anketa
		self.assertBodyTextPresent(u"Обязательно укажите какие-нибудь свои координаты")
		
# def main():
selenium_test.RunTest(XcmsOpenRenamedPages())
    