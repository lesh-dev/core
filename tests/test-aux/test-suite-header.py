#!/usr/bin/python
# -*- coding: utf8 -*-
from selenium_test import RunTest
import test_xcms_installer
import sys

def getOption(opt, args):
	for i in xrange(0, len(args)-1):
		if args[i] == opt:
			del args[i]
			value = args[i+1]
			del args[i+1]
			return value, args
	return None, args

def getSingleOption(opt, args):
	for i in xrange(0, len(args)):
		if args[i] == opt:
			del args[i]
			return True, args
	return False, args

args = sys.argv[1:] # exclude program name

installerTest, args = getSingleOption("-i", args)

specTest, args = getOption("-t", args)

# last remaining argument is base test URL.

if len(args) < 1:
	print "Base tests URL is not set. Usage:"
	print "auto-test-suite.py <test-site-url>"
	sys.exit(1)

baseUrl = args.pop()

print "Running tests on base URL", baseUrl

if installerTest:
	print "Running installer test. "
	RunTest(test_xcms_installer.TestXcmsInstaller())

## here should be auto-generated imports and test list
## here should be code from footer.
