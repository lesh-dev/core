#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test, tests_common
from xcms_test_config import XcmsTestConfig

try:
	test = selenium_test.SeleniumTest("xcms-auth-root-login", sys.argv[1])
	
	test.setAutoPhpErrorChecking(True)
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
	conf = XcmsTestConfig()
	
	tests_common.performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
	
	test.gotoUrlByLinkText(u"Админка")
	
	test.assertBodyTextPresent(u"Пользователи")
	test.assertBodyTextPresent(u"Очистить кэш")
	
except RuntimeError as e:
	selenium_test.printTestFailResult(e)
	if "-d" in sys.argv or "--debug" in sys.argv:
		print "Details: "
		traceback.print_exc()
	#else:
		#traceback.print_exc(1)
	sys.exit(1)
except Exception as e:
	print "TEST ERROR:", e
	traceback.print_exc()
	sys.exit(2)
    