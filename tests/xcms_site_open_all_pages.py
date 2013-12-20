#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsSiteOpenAllPages(xtest_common.XcmsTest):
	"""
	This test checks overall site content.
	It does following steps:
	* navigates to all current pages and checks some specific content on each page plus PHP errors.
	"""
	def run(self):
		self.gotoRoot()
		
		self.gotoUrlByLinkText(u"Главная")
		self.assertBodyTextPresent(u"Приветствуем Вас на сайте Физического отделения Летней Экологической Школы");

		self.gotoUrlByLinkText(u"История ЛЭШ")
		self.assertBodyTextPresent(u"Школа существует достаточно давно")

		self.gotoUrlByLinkText(u"Новости")
		self.assertBodyTextPresent(u"Новости")

		self.gotoUrlByLinkText(u"Официально о ЛЭШ")
		self.assertBodyTextPresent(u"Официальная информация")
		self.assertBodyTextPresent(u"Летняя Экологическая Школа (ЛЭШ) существует с 1990 года")

		self.gotoUrlByPartialLinkText(u"Набор на Школу - 201")

		self.gotoUrlByLinkText(u"О нас")
		self.assertBodyTextPresent(u"О нас")

		self.gotoUrlByLinkText(u"Жизнь на ЛЭШ")
		self.assertBodyTextPresent(u"Жизнь на ЛЭШ")

		self.gotoUrlByLinkText(u"Список вещей")
		self.gotoPage("/gear")
		self.assertBodyTextPresent(u"Список вещей")
		self.assertBodyTextPresent(u"Снаряжение")

		self.gotoUrlByLinkText(u"Снаряжение")
		self.assertBodyTextPresent(u"Туристическое снаряжение на ЛЭШ")
		self.assertBodyTextPresent(u"Спальник")
		self.gotoPage("/gear/equipment")
		self.assertBodyTextPresent(u"Туристическое снаряжение на ЛЭШ")
		self.assertBodyTextPresent(u"Палатка")
		
		self.gotoUrlByLinkText(u"Личные вещи и одежда")
		self.assertBodyTextPresent(u"Личные вещи и одежда")
		self.gotoPage("/gear/wear")
		self.assertBodyTextPresent(u"Кружка, Ложка, Миска, Нож.")
		
		
		self.gotoUrlByLinkText(u"Документы")
		self.assertBodyTextPresent(u"Полис ОМС")
		self.gotoPage("/gear/docs")
		self.assertBodyTextPresent(u"Справка из СЭС об отсутствии контактов")

		self.gotoUrlByLinkText(u"Прочее")
		self.assertBodyTextPresent(u"Фонарик")
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
		
		self.gotoUrlByLinkText(u"Главная")
		
    