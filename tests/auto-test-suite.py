#!/usr/bin/python
# -*- coding: utf8 -*-

# WARNING! This file is AUTO-GENERATED. Do not edit it directly, edit header/footer/generator instead.

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
 
import xcms_auth_add_new_user
import xcms_auth_check_dup_email
import xcms_auth_check_dup_login
import xcms_auth_root_login
import xcms_download_lectures
import xcms_metrics_check
import xcms_open_all_pages
import xcms_open_non_existing
import xcms_open_renamed_pages
import xcms_unittests
import xcms_version_check
import xcms_xsm_anketa_fill
tests = [
xcms_auth_add_new_user.XcmsAuthAddNewUser(baseUrl),
xcms_auth_check_dup_email.XcmsAuthCheckDupEmail(baseUrl),
xcms_auth_check_dup_login.XcmsAuthCheckDupLogin(baseUrl),
xcms_auth_root_login.XcmsAuthRootLogin(baseUrl),
xcms_download_lectures.XcmsDownloadLectures(baseUrl),
xcms_metrics_check.XcmsMetricsCheck(baseUrl),
xcms_open_all_pages.XcmsOverallOpenPages(baseUrl),
xcms_open_non_existing.XcmsOpenNonExisting(baseUrl),
xcms_open_renamed_pages.XcmsOpenRenamedPages(baseUrl),
xcms_unittests.XcmsUnitTests(baseUrl),
xcms_version_check.XcmsVersionCheck(baseUrl),
xcms_xsm_anketa_fill.XcmsXsmAnketaFill(baseUrl),
]

				
while len(tests) > 0:
	test = tests.pop()
	if specTest and test.getName() != specTest: continue
	print "Running test", test.getName()
	print test.getDoc()
	RunTest(test)


