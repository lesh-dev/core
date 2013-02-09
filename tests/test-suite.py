#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium_test import RunTest, TestShutdown
import test_xcms_installer
import sys

from bawlib import getOption, getSingleOption, isVoid

def showHelp():
	print "Parameters not specified."
	print "Common usage:"
	print "\ttest-suite.py [-i] [TEST OPTIONS] <site-url>"
	print "Run specific test:"
	print "\ttest-suite.py -t <test-name> [TEST OPTIONS] <site-url>"
	print ""
	print "Examples:"
	print "test-suite.py test.fizlesh.ru"
	print "test-suite.py -t XcmsXsmAnketaFill test.fizlesh.ru"
	print ""
	print "OPTIONS:"
	print "-i\t\tRun installer test prior to all rest suite"
	print "-h, --help\tDisplay this help"
	print "-t\t\tRun specific test instead of all suite"
	print ""
	print "TEST OPTIONS could be test-dependent. Commonly supported options are: "
	print "-l, --leave-open\t\tLeave browser window after test finish/fail"
	print "-d, --doc\t\t\tDisplay test documentation"
	
	
args = sys.argv[1:] # exclude program name

doInstallerTest, args = getSingleOption(["-i", "--installer"], args)

specTest, args = getOption(["-t", "--test"], args)

doShowHelp, args = getOption(["-h", "--help"], args)

testSet, args = getOption(["-s", "--set"], args)

# last remaining argument is base test URL.

if len(args) < 1:
	showHelp()
	sys.exit(1)

baseUrl = args.pop()

if isVoid(baseUrl):
	showHelp()
	sys.exit(1)

if doInstallerTest:
	print "Running installer test. "
	RunTest(test_xcms_installer.TestXcmsInstaller(baseUrl, args))
 
setModuleName = "auto_test_set"

if testSet:
	setModuleName = testSet.replace(".py", "")
	
testSetModule = __import__(setModuleName, [])	

try:
	tests = testSetModule.getTests(baseUrl, args)
	while len(tests) > 0:
		test = tests.pop()
		if specTest and test.getName() != specTest:
			continue
		print "Running test", test.getName()
		print test.getDoc()
		RunTest(test)

except TestShutdown as e:
	pass


