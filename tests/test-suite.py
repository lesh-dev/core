#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium_test import RunTest

import xcms_auth_add_new_user
import xcms_auth_root_login
import xcms_download_lectures
import xcms_metrics_check
import xcms_open_all_pages
import xcms_open_non_existing
import xcms_open_renamed_pages
import xcms_unittests
import xcms_version_check
import xcms_xsm_anketa_fill

# def main():
tests = [
	#xcms_auth_add_new_user.XcmsAuthAddNewUser(), 
	xcms_auth_root_login.XcmsAuthRootLogin(), 
	xcms_download_lectures.XcmsDownloadLectures(),
	xcms_metrics_check.XcmsMetricsCheck(),
	xcms_unittests.XcmsUnitTests()
	]
	
for test in tests:
	print test.__doc__
	RunTest(test)
	del test


