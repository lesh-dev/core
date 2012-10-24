#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test, tests_common

try:
	test = selenium_test.SeleniumTest("xcms-auth-add-new-user")
	
	#this test logins as admin and adds new user to XCMS.
	
	test.autoErrorCheckingOn()
	if "-l" in sys.argv or "--leave-open" in sys.argv:
		test.setCloseOnExit(False)
	
# first, login as admin
	tests_common.performLoginAsAdmin(test, "root", "root")
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
    