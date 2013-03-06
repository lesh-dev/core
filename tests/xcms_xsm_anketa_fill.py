#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsXsmAnketaFill(SeleniumTest):
	"""
	This test checks anketa add functional.
	It does following steps:
	* navigates to anketa form
	* fill anketa with all correct values
	* submits form
	* login as admin (root)
	* naviagates to anketa list
	* clicks on new anketa
	* checks if all enetered data match screen form.
	"""
	
	def run(self):
		# anketa fill positive test:
		# all fields are filled with correct values.
		conf = XcmsTestConfig()
		
		adminLogin = conf.getAdminLogin()
		adminPass = conf.getAdminPass()
		
		testMailPrefix = conf.getAnketaNamePrefix()
			
		self.setAutoPhpErrorChecking(True)
		
		xtest_common.assertNoInstallerPage(self)

		self.gotoRoot()
		
		#navigate to anketas
		
		self.gotoUrlByLinkText(u"Поступление")
		self.gotoUrlByLinkText(u"Анкета")
		self.assertBodyTextPresent(u"Регистрационная анкета")
			
		# generate
		inpLastName = testMailPrefix + u"Чапаев" + random_crap.randomText(5);
		inpFirstName = u"Василий" + random_crap.randomText(3)
		inpMidName = u"Иваныч" + random_crap.randomText(3)
		
		inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4);
		
		inpSchool = u"Тестовая школа им. В.Е.Бдрайвера №" + random_crap.randomDigits(4)
		
		inpSchoolCity = u"Школа находится в /var/opt/" + random_crap.randomText(5)
		inpClass = random_crap.randomDigits(1) + u" Гэ"
		
		inpPhone = "+7" + random_crap.randomDigits(9)
		inpCell = "+7" + random_crap.randomDigits(9)
		inpEmail = random_crap.randomText(10) + "@" + random_crap.randomText(6) + ".ru"
		inpSkype = random_crap.randomText(12)
		inpSocial = random_crap.randomVkontakte()
		
		inpFav = random_crap.randomCrap(20)
		inpAch = random_crap.randomCrap(15)
		inpHob = random_crap.randomCrap(10)
		
		inpLastName = self.fillElementById("last_name-input", inpLastName)
		
		inpFirstName = self.fillElementById("first_name-input", inpFirstName)
		inpMidName = self.fillElementById("patronymic-input", inpMidName)
		inpBirthDate = self.fillElementById("birth_date-input", inpBirthDate)
		inpSchool = self.fillElementById("school-input", inpSchool)
		inpSchoolCity = self.fillElementById("school_city-input", inpSchoolCity)
		inpClass = self.fillElementById("current_class-input", inpClass)
		inpPhone = self.fillElementById("phone-input",inpPhone)
		inpCell = self.fillElementById("cellular-input", inpCell)
		inpEmail = self.fillElementById("email-input", inpEmail)
		inpSkype = self.fillElementById("skype-input", inpSkype)
		inpSocial = self.fillElementById("social_profile-input", inpSocial)
		inpFav = self.fillElementById("favourites-text", inpFav)
		inpAch = self.fillElementById("achievements-text", inpAch)
		inpHob = self.fillElementById("hobby-text", inpHob)
		
		self.clickElementById("submit-anketa-button")
		
		self.assertBodyTextPresent(u"Спасибо, Ваша анкета принята!")
		
			
	# now login as admin
		xtest_common.performLoginAsAdmin(self, adminLogin, adminPass)
		
		self.gotoRoot()
			
		self.gotoUrlByLinkText(u"Анкеты")
		
		fullAlias = inpLastName + " " + inpFirstName
		#+ " " + inpMidName
		#print "Full student alias:", fullAlias.encode("utf-8")
		anketaUrlName = fullAlias.strip()
		# try to drill-down into table with new anketa.

		self.gotoUrlByLinkText(anketaUrlName)

	# just check text is on the page.
		print "Checking that all filled fields are displayed on the page. "
		
		self.assertBodyTextPresent(fullAlias)
		self.assertBodyTextPresent(inpBirthDate)
		self.assertBodyTextPresent(inpSchool)
		self.assertBodyTextPresent(inpSchoolCity)
		self.assertBodyTextPresent(inpClass)
		self.assertBodyTextPresent(inpPhone)
		self.assertBodyTextPresent(inpCell)
		self.assertBodyTextPresent(inpEmail)
		self.assertBodyTextPresent(inpSkype)
		self.assertBodyTextPresent(inpSocial)
		self.assertBodyTextPresent(inpFav)
		self.assertBodyTextPresent(inpAch)
		self.assertBodyTextPresent(inpHob)	
	