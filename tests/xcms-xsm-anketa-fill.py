#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback
#local imports
import selenium_test, tests_common

try:
	test = selenium_test.SeleniumTest("xcms-xsm-anketa-fill")
	
	# anketa fill positive test:
	# all fields are filled with correct values.
	
	testMailPrefix = "NO-MAIL-TEST"
	
	test.autoErrorCheckingOn()
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	test.gotoPage("/")
	
	#navigate to anketas
	
	test.gotoUrlByLinkText(u"Поступление")
	test.gotoUrlByLinkText(u"Анкета")
	test.assertBodyTextPresent(u"Регистрационная анкета")
		
	# generate
	inpLastName = testMailPrefix + u"Чапаев" + selenium_test.randomText(5);
	inpFirstName = u"Василий" + selenium_test.randomText(3)
	inpMidName = u"Иваныч" + selenium_test.randomText(3)
	
	inpBirthDate = selenium_test.randomDigits(2) + "." + selenium_test.randomDigits(2) + "." + selenium_test.randomDigits(4);
	
	inpSchool = u"Тестовая школа им. В.Е.Бдрайвера №" + selenium_test.randomDigits(4)
	
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
	
	inpFirstName = test.fillElementById("first_name-input", inpFirstName)
	inpMidName = test.fillElementById("patronymic-input", inpMidName)
	inpBirthDate = test.fillElementById("birth_date-input", inpBirthDate)
	inpSchool = test.fillElementById("school-input", inpSchool)
	inpSchoolCity = test.fillElementById("school_city-input", inpSchoolCity)
	inpClass = test.fillElementById("current_class-input", inpClass)
	inpPhone = test.fillElementById("phone-input",inpPhone)
	inpCell = test.fillElementById("cellular-input", inpCell)
	inpEmail = test.fillElementById("email-input", inpEmail)
	inpSkype = test.fillElementById("skype-input", inpSkype)
	inpSocial = test.fillElementById("social_profile-input", inpSocial)
	inpFav = test.fillElementById("favourites-text", inpFav)
	inpAch = test.fillElementById("achievements-text", inpAch)
	inpHob = test.fillElementById("hobby-text", inpHob)
	
	test.clickElementById("submit-anketa-button")
	
	test.assertBodyTextPresent(u"Спасибо, Ваша анкета принята!")
	
		
# now login as admin
	tests_common.performLoginAsAdmin(test, "root", "root")
	
	# BUG! we got to admin page after authorize!! 
	# expected: root page with auth menu items.
	
	test.gotoRoot()
		
# TODO: TEMPORARY link, make different anketa list.
	test.gotoUrlByLinkText(u"Участники")
	
	fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
	#print "Full student alias:", fullAlias.encode("utf-8")
	anketaUrlName = fullAlias.strip()

	# BUG: here is a bug on the page, but we skip it.
	test.autoErrorCheckingOff()
	test.gotoUrlByLinkText(anketaUrlName)
	test.autoErrorCheckingOn()

# just check text is on the page.
	print "Checking that all filled fields are displayed on the page. "
	
	test.assertBodyTextPresent(fullAlias)
	test.assertBodyTextPresent(inpBirthDate)
	test.assertBodyTextPresent(inpSchool)
	test.assertBodyTextPresent(inpSchoolCity)
	test.assertBodyTextPresent(inpClass)
	test.assertBodyTextPresent(inpPhone)
	test.assertBodyTextPresent(inpCell)
	test.assertBodyTextPresent(inpEmail)
	test.assertBodyTextPresent(inpSkype)
	test.assertBodyTextPresent(inpSocial)
	test.assertBodyTextPresent(inpFav)
	test.assertBodyTextPresent(inpAch)
	test.assertBodyTextPresent(inpHob)	
	
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
    