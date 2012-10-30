#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback
#local imports
import selenium_test, tests_common

try:
	test = selenium_test.SeleniumTest("test-installer", sys.argv[1])
	# TODO: wait for fix of installer HTML testability.
	
	
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
    