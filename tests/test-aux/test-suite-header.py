#!/usr/bin/python
# -*- coding: utf8 -*-

# ##auto_generated_warning_placeholder##

from selenium_test import RunTest
import test_xcms_installer
import sys

def getOption(opt, args):
	for i in xrange(0, len(args)-1):
		if args[i] == opt:
			del args[i]
			value = args[i]
			del args[i]
			return value, args
	return None, args

def getSingleOption(opt, args):
	for i in xrange(0, len(args)):
		if args[i] == opt:
			del args[i]
			return True, args
	return False, args


def showHelp():
	print "Parameters not specified. Usage:"
	print "auto-test-suite.py [-i] [-t <test-name>] <site-url>"
	print ""
	print "Example: auto-test-suite test.fizlesh.ru"
	print ""
	print "OPTIONS:"
	print "-i\t\tRun installer test prior to rest suite"
	print "-t <test-name>\t\tRun specific test named <test-name>"
	
args = sys.argv[1:] # exclude program name

installerTest, args = getSingleOption("-i", args)

specTest, args = getOption("-t", args)

# last remaining argument is base test URL.

if len(args) < 1:
	showHelp()
	sys.exit(1)

baseUrl = args.pop()

if baseUrl.strip() == "":
	showHelp()
	sys.exit(1)

print "Running tests on base URL", baseUrl

if installerTest:
	print "Running installer test. "
	RunTest(test_xcms_installer.TestXcmsInstaller())
