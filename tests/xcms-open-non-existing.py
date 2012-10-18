#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test

debugMode = True #"TRUE" in os.getenv("XCMS_TEST_DEBUG");

try:
	test = selenium_test.SeleniumTest()
	test.gotoPage("/qqq");
	test.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
	homeHref = test.getUrlByLinkText(u"этой ссылке")
	print "Home reference on 404 page: ", homeHref
	
	test.gotoSite(homeHref)
	
except RuntimeError as e:
	print "TEST FAILED: ", e
	print "Last step: ", traceback.print_exc(1)
	sys.exit(1)
except Exception as e:
	print "TEST ERROR: ", e
	traceback.print_exc()
	sys.exit(2)
    