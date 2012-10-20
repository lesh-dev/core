#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test

try:
	test = selenium_test.SeleniumTest()
	
	test.autoErrorCheckingOn()
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	test.gotoPage("/")
	test.assertBodyTextPresent(u"Авторизация")
	
	authUrl = test.getUrlByLinkText(u"Авторизация")
	
	print "Auth URL:", authUrl
	test.gotoSite(authUrl)
	
	test.assertSourceTextPresent(u"Логин")
	test.assertSourceTextPresent(u"Пароль")
	test.assertSourceTextPresent(u"Требуется аутентификация")
	
	#<input type="text" name="auth-login" />
	#ele = test.drv().find_element_by_name("auth-login")
	test.fillElementByName("auth-login", "root")
	test.fillElementByName("auth-password", "root")
	
	test.clickElementByName("auth-form")
	
	cpUrl = test.getUrlByLinkText(u"Админка")
	test.gotoSite(cpUrl)
	
	test.assertBodyTextPresent(u"Пользователи")
	test.assertBodyTextPresent(u"Очистить кэш")
	
	
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
    