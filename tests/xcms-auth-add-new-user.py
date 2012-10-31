#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test, tests_common

from xcms_test_config import XcmsTestConfig

try:
	test = selenium_test.SeleniumTest("xcms-auth-add-new-user", sys.argv[1])
	
	#this test logins as admin and adds new user to XCMS.
	
	test.setAutoPhpErrorChecking(True)
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	conf = XcmsTestConfig()
	
# first, login as admin
	print "logging as admin"
	tests_common.performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
	
	print "go to user creation panel"
	
	#	test.gotoRoot()
	test.gotoUrlByLinkText(u"Админка")
	# navigate to users CP
	print "goto user list."
	test.gotoUrlByLinkText(u"Пользователи")
	test.assertBodyTextPresent(u"Администрирование пользователей")
	test.gotoUrlByLinkText("Create user")
	
	
	inpLogin = "an_test_user_" + selenium_test.randomText(8)
	inpEMail = selenium_test.randomEmail()
	inpPass1 = selenium_test.randomText(10)
	inpPass2 = inpPass1
	inpName = u"Вася Пупкин" + selenium_test.randomText(6)
	#inpName = u"Вася Пупкин" + selenium_test.randomText(6)
	
	#<tr><td colspan="2"><b>Учетные данные</b>                               </td></tr>
	#<tr><td>Имя пользователя:   </td><td> <input name="login">                </td></tr>
	#<tr><td>Пароль:             </td><td> <input type="password" name="p1">   </td></tr>
	#<tr><td>Пароль  (еще раз):  </td><td> <input type="password" name="p2">   </td></tr>
	#<tr><td>Настоящее имя:      </td><td> <input name="name">                 </td></tr>
	#<tr><td>Электропочта:       </td><td> <input name="email">                </td></tr>
	#<tr><td colspan="2">  <input type="checkbox" name="notify_user" />	
	inpLogin = test.fillElementByName("login", inpLogin)
	inpEMail = test.fillElementByName("email", inpEMail)
	inpPass1 = test.fillElementByName("p1", inpPass1)
	inpPass2 = test.fillElementByName("p2", inpPass2)
	inpPass1 = test.fillElementByName("name", inpName)
	
	# set notify checkbox.
	test.clickElementByName("notify_user")
	# send form
	
	test.clickElementByName("create_user")
	
	print "user created, going to user list again to refresh. "
	
	# here is a usability issue: user not appears in the list.
	# refresh user list
	test.gotoUrlByLinkText(u"Пользователи")
	
	test.gotoUrlByLinkText(inpLogin)
	
	test.assertBodyTextPresent(u"Известен под логином " + inpLogin)
	
	print "logging as created user. "
	tests_common.performLogin(test, inpLogin, inpPass1)	
	
except selenium_test.TestError as e:
	selenium_test.printTestFailResult(e)
	sys.exit(1)
except Exception as e:
	print "TEST INTERNAL ERROR:", e
	traceback.print_exc()
	sys.exit(2)
    