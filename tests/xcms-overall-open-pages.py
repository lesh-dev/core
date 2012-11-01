#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsOverallOpenPages(SeleniumTest):
	"""
	This test checks overall site content.
	It does following steps:
	* navigates to all current pages and checks some specific content on each page plus PHP errors.
	"""
	def run(self):
		
	self.setAutoPhpErrorChecking(True)
#	self.setCloseOnExit(False)
	
	self.gotoPage("/")
	
	self.assertBodyTextPresent(u"Здравствуйте!");
	self.assertBodyTextPresent(u"Приветствуем Вас на сайте Физического отделения Летней Экологической Школы");

	self.gotoPage("/news")
	self.assertBodyTextPresent(u"Новости")
	
	self.gotoPage("/history")
	self.assertBodyTextPresent(u"Школа существует достаточно давно")

	self.gotoPage("/info")
	self.assertBodyTextPresent(u"Официальная информация")
	self.assertBodyTextPresent(u"Летняя Экологическая Школа (ЛЭШ) существует с 1990 года")
	
	self.gotoPage("/people")
	self.assertBodyTextPresent(u"О нас")

	self.gotoPage("/life")
	self.assertBodyTextPresent(u"Жизнь на ЛЭШ")

	self.gotoPage("/gear")
	self.assertBodyTextPresent(u"Список вещей")

	self.gotoPage("/gear/equipment")
	self.assertBodyTextPresent(u"Туристическое снаряжение на ЛЭШ")

	self.gotoPage("/gear/wear")
	self.assertBodyTextPresent(u"Личные вещи и одежда")

	self.gotoPage("/gear/wear")
	self.assertBodyTextPresent(u"Личные вещи и одежда")
	self.assertBodyTextPresent(u"КЛМН - Кружка, Ложка, Миска, Нож.")
	
	
	self.gotoPage("/gear/docs")
	self.assertBodyTextPresent(u"Справка из СЭС об отсутствии контактов")

	self.gotoPage("/gear/misc")
	self.assertBodyTextPresent(u"А еще я обычно беру с собой")

	self.gotoPage("/study")
	self.assertBodyTextPresent(u"Особенности ЛЭШевского образования")

	self.gotoPage("/study/2006")
	self.gotoPage("/study/2007")
	self.gotoPage("/study/2008")
	self.gotoPage("/study/2009")
	self.gotoPage("/study/2010")
	self.gotoPage("/study/2011")
	self.gotoPage("/study/lectures2011")
	self.gotoPage("/study/2012")
	self.gotoPage("/study/experiment")
	self.assertBodyTextPresent(u"Здесь приведены задачи физического практикума")
	self.gotoPage("/science")

	self.gotoPage("/join")
	self.assertBodyTextPresent(u"Собеседование на Физическое Отделение")
	self.gotoPage("/register")
	self.assertBodyTextPresent(u"Регистрационная анкета")
	self.gotoPage("/photo")
	self.gotoPage("/fun")
	self.gotoPage("/links")
	self.gotoPage("/contacts")
		
#	self.assertPhpErrors()

# def main():
selenium_test.RunTest(XcmsOverallOpenPages())
    