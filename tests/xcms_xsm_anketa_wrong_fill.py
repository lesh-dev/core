#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsXsmAnketaWrongFill(SeleniumTest):
	"""
	This test checks bad cases of anketa add functional
	It does following:
	* navigate to anketa form
	* fill anketa with incorrect values
	* try to submit form
	* correct some values and try submit again
	* correct all errors and finally submit form.
	"""
	
	def tryWrongSubmit(self, forbidReason):
		submitOkMsg = u"Спасибо, Ваша анкета принята!"
		self.clickElementById("submit-anketa-button")
		self.assertBodyTextNotPresent(submitOkMsg, forbidReason)
	
	def run(self):
		# anketa fill negative test:
		
		self.setAutoPhpErrorChecking(True)
		xtest_common.assertNoInstallerPage(self)

		conf = XcmsTestConfig()
		
		testMailPrefix = conf.getAnketaNamePrefix()
			
		self.gotoRoot()
		
		#navigate to anketas
		
		self.gotoUrlByLinkText(u"Поступление")
		self.gotoUrlByLinkText(u"Анкета")
		self.assertBodyTextPresent(u"Регистрационная анкета")
			
		# try to submit empty form.
		self.tryWrongSubmit("Empty form should not be submitted. ")
		self.assertBodyTextPresent(u"Поле 'Фамилия' слишком короткое")

		# generate some text
		inpLastName = testMailPrefix + u"Криворучкин" + random_crap.randomText(5);
		inpFirstName = u"Хакер" + random_crap.randomText(3)
		inpMidName = u"Ламерович" + random_crap.randomText(3)
		
		inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4);
		
		inpSchool = u"Хакерская школа им. К.Митника №" + random_crap.randomDigits(4)
		
		inpSchoolCity = u"Школа находится в /dev/brain/" + random_crap.randomText(5)
		inpClass = random_crap.randomDigits(1) + u"Х"
		
		inpPhone = "+7" + random_crap.randomDigits(9)
		inpCell = "+7" + random_crap.randomDigits(9)
		inpEmail = random_crap.randomText(10) + "@" + random_crap.randomText(6) + ".com"
		inpSkype = random_crap.randomText(12)
		inpSocial = random_crap.randomVkontakte()
		
		inpFav = random_crap.randomCrap(20, ["multiline"])
		inpAch = random_crap.randomCrap(15, ["multiline"])
		inpHob = random_crap.randomCrap(10, ["multiline"])
		
		# try fill only surname 
		inpLastName = self.fillElementById("last_name-input", inpLastName)
		
		self.tryWrongSubmit("Only Last name was filled. ")
		self.assertBodyTextPresent(u"Поле 'Имя' слишком короткое")
		
		inpFirstName = self.fillElementById("first_name-input", inpFirstName)
		
		self.tryWrongSubmit("Only Last name and First name was filled. ")
		self.assertBodyTextPresent(u"Поле 'Отчество' слишком короткое")

		inpMidName = self.fillElementById("patronymic-input", inpMidName)

		self.tryWrongSubmit("Only FIO values were filled. ")
		self.assertBodyTextPresent(u"Класс не указан")
		
		inpBirthDate = self.fillElementById("birth_date-input", inpBirthDate)
		inpSchool = self.fillElementById("school-input", inpSchool)
		inpSchoolCity = self.fillElementById("school_city-input", inpSchoolCity)
		
		inpClass = self.fillElementById("current_class-input", inpClass)

		self.tryWrongSubmit("Phone fields were not filled. ")
		self.assertBodyTextPresent(u"Укажите правильно хотя бы один из телефонов")

		inpPhone = self.fillElementById("phone-input",inpPhone)
		inpCell = self.fillElementById("cellular-input", inpCell)
		
		inpEmail = self.fillElementById("email-input", inpEmail)
		inpSkype = self.fillElementById("skype-input", inpSkype)
		inpSocial = self.fillElementById("social_profile-input", inpSocial)

		self.tryWrongSubmit("Favourites were not filled")
		self.assertBodyTextPresent(u"Если Вы уверены, что не хотите указывать эту информацию")

		inpFav = self.fillElementById("favourites-text", inpFav)
		self.tryWrongSubmit("Achievements were not filled")
		self.assertBodyTextPresent(u"Если Вы уверены, что не хотите указывать эту информацию")

		inpAch = self.fillElementById("achievements-text", inpAch)
		self.tryWrongSubmit("Hobbies were not filled")
		self.assertBodyTextPresent(u"Если Вы уверены, что не хотите указывать эту информацию")

		inpHob = self.fillElementById("hobby-text", inpHob)
		
		# and now try to erase one of very important  fields.
		
		self.fillElementById("last_name-input", "")
		
		self.tryWrongSubmit("Empty last name is not allowed. ")
		self.assertBodyTextPresent(u"Поле 'Фамилия' слишком короткое")

		# fill it again.
		inpLastName = self.fillElementById("last_name-input", inpLastName)

		self.fillElementById("hobby-text", "")

		self.tryWrongSubmit("Hobbies were erased")
		self.assertBodyTextPresent(u"Если Вы уверены, что не хотите указывать эту информацию")
		# no erase achievements.
		self.fillElementById("achievements-text", "")
		self.tryWrongSubmit("Enter confirmation mode with erased field 'A' and remove another field 'B'. Revalidation check after bug #529")

		inpHob = self.fillElementById("hobby-text", inpHob)
		inpAch = self.fillElementById("achievements-text", inpAch)

		# at last, it should work.
		self.clickElementById("submit-anketa-button")
		self.assertBodyTextPresent(u"Спасибо, Ваша анкета принята!")
			
		# now login as admin
	
		adminLogin = conf.getAdminLogin()
		adminPass = conf.getAdminPass()

		xtest_common.performLoginAsAdmin(self, adminLogin, adminPass)
		
		self.gotoRoot()
			
		self.gotoUrlByLinkText(u"Анкеты")
		
		fullAlias = inpLastName + " " + inpFirstName

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
		self.clickElementById("show-extra-person-info")
		self.wait(1)
		self.assertBodyTextPresent(inpFav)
		self.assertBodyTextPresent(inpAch)
		self.assertBodyTextPresent(inpHob)
