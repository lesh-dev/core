#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback
#local imports
import selenium_test, tests_common

try:
	test = selenium_test.SeleniumTest()
	
	test.autoErrorCheckingOn()
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	test.gotoPage("/")
	
	#navigate to anketas
	
	test.gotoUrlByLinkText(u"Поступление")
	test.gotoUrlByLinkText(u"Анкета")
	test.assertBodyTextPresent(u"Регистрационная анкета")
	
	# generate
	inpLastName = u"NO-MAIL-TEST Чапаев" + selenium_test.randomText(5);
	inpFirstName = u"Василий" + selenium_test.randomText(3)
	inpMidName = u"Иваныч" + selenium_test.randomText(3)
	
	inpBirthDate = selenium_test.randomDigits(2) + "." + selenium_test.randomDigits(2) + "." + selenium_test.randomDigits(4);
	
	inpSchool = u"Тестовая школа им. В.Е.Бдрайвера №"# + selenium_test.randomDigits(4)
	
	inpSchoolCity = u"Школа находится в /var/opt/" + selenium_test.randomText(5)
	inpClass = selenium_test.randomDigits(1) + u" Гэ"
	
	inpPhone = "+7" + selenium_test.randomDigits(9)
	inpCell = "+7" + selenium_test.randomDigits(9)
	inpEmail = selenium_test.randomText(10) + "@" + selenium_test.randomText(6) + ".ru"
	inpSkype = selenium_test.randomText(12)
	inpSocial = "http://vk.com/" + selenium_test.randomText(8)
	
	inpFav = selenium_test.randomCrap(20)
	inpAch = selenium_test.randomCrap(15)
	inpHob = selenium_test.randomCrap(10)
	
	inpLastName = test.fillElementById("last_name-input", inpLastName)
	print "LastName = ", inpLastName
	
	test.fillElementById("first_name-input", inpFirstName)
	test.fillElementById("patronymic-input", inpMidName)
	test.fillElementById("birth_date-input", inpBirthDate)
	test.fillElementById("school-input", inpSchool)
	test.fillElementById("school_city-input", inpSchoolCity)
	test.fillElementById("current_class-input", inpClass)
	test.fillElementById("phone-input",inpPhone)
	test.fillElementById("cellular-input", inpCell)
	test.fillElementById("email-input", inpEmail)
	test.fillElementById("skype-input", inpSkype)
	test.fillElementById("social_profile-input", inpSocial)
	test.fillElementById("favourites-text", inpFav)
	test.fillElementById("achievements-text", inpAch)
	test.fillElementById("hobby-text", inpHob)
	
	test.clickElementById("submit-anketa-button")
	
	test.assertBodyTextPresent(u"Спасибо, Ваша анкета принята!")
	
		
# first, login as admin
#	tests_common.performLoginAsAdmin(test, "root", "root")
	
# navigate to users CP
	
	
	
except RuntimeError as e:
	print "TEST FAILED:", e
	print "Last test command: "
	if "-d" in sys.argv or "--debug" in sys.argv:
		traceback.print_exc()
	else:
		traceback.print_exc(1)
	sys.exit(1)
except Exception as e:
	print "TEST ERROR:", e
	traceback.print_exc()
	sys.exit(2)
    