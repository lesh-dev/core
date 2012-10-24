#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test, tests_common

try:
	test = selenium_test.SeleniumTest("xcms-auth-root-login")
	
	test.autoErrorCheckingOn()
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	tests_common.performLoginAsAdmin(test, "root", "root")
	
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
    