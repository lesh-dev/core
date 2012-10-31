#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test

try:
	test = selenium_test.SeleniumTest("xcms-overall-open-pages", sys.argv[1])
	
	test.setAutoPhpErrorChecking(True)
#	test.setCloseOnExit(False)
	
	test.gotoPage("/")
	
	test.assertBodyTextPresent(u"Здравствуйте!");
	test.assertBodyTextPresent(u"Приветствуем Вас на сайте Физического отделения Летней Экологической Школы");

	test.gotoPage("/news")
	test.assertBodyTextPresent(u"Новости")
	
	test.gotoPage("/history")
	test.assertBodyTextPresent(u"Школа существует достаточно давно")

	test.gotoPage("/info")
	test.assertBodyTextPresent(u"Официальная информация")
	test.assertBodyTextPresent(u"Летняя Экологическая Школа (ЛЭШ) существует с 1990 года")
	
	test.gotoPage("/people")
	test.assertBodyTextPresent(u"О нас")

	test.gotoPage("/life")
	test.assertBodyTextPresent(u"Жизнь на ЛЭШ")

	test.gotoPage("/gear")
	test.assertBodyTextPresent(u"Список вещей")

	test.gotoPage("/gear/equipment")
	test.assertBodyTextPresent(u"Туристическое снаряжение на ЛЭШ")

	test.gotoPage("/gear/wear")
	test.assertBodyTextPresent(u"Личные вещи и одежда")

	test.gotoPage("/gear/wear")
	test.assertBodyTextPresent(u"Личные вещи и одежда")
	test.assertBodyTextPresent(u"КЛМН - Кружка, Ложка, Миска, Нож.")
	
	
	test.gotoPage("/gear/docs")
	test.assertBodyTextPresent(u"Справка из СЭС об отсутствии контактов")

	test.gotoPage("/gear/misc")
	test.assertBodyTextPresent(u"А еще я обычно беру с собой")

	test.gotoPage("/study")
	test.assertBodyTextPresent(u"Особенности ЛЭШевского образования")

	test.gotoPage("/study/2006")
	test.gotoPage("/study/2007")
	test.gotoPage("/study/2008")
	test.gotoPage("/study/2009")
	test.gotoPage("/study/2010")
	test.gotoPage("/study/2011")
	test.gotoPage("/study/lectures2011")
	test.gotoPage("/study/2012")
	test.gotoPage("/study/experiment")
	test.assertBodyTextPresent(u"Здесь приведены задачи физического практикума")
	test.gotoPage("/science")

	test.gotoPage("/join")
	test.assertBodyTextPresent(u"Собеседование на Физическое Отделение")
	test.gotoPage("/register")
	test.assertBodyTextPresent(u"Регистрационная анкета")
	test.gotoPage("/photo")
	test.gotoPage("/fun")
	test.gotoPage("/links")
	test.gotoPage("/contacts")
		
#	test.assertPhpErrors()
	
except RuntimeError as e:
	print "TEST FAILED:", e
	print "Last test command: "
	if "--debug" in sys.argv:
		traceback.print_exc()
	else:
		traceback.print_exc(1)
	sys.exit(1)
except Exception as e:
	print "TEST ERROR:", e
	traceback.print_exc()
	sys.exit(2)
    