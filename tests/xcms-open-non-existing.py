#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

debugMode = True #"TRUE" in os.getenv("XCMS_TEST_DEBUG");

driver = webdriver.Firefox()

try:
#	print dir(driver)

	baseUrl = "http://rc.fizlesh.ru/"
	driver.get(baseUrl + "/qqq")

	# expect error page
	errorDiv = driver.find_element_by_xpath("//div[@class='error-widget']")

	#print errorDiv.text

	if u"Нет такой страницы" not in errorDiv.text:
		raise RuntimeError("Wrong page opened on non-existing URL")
	
	homeUrl = driver.find_element_by_link_text("этой ссылке")
	
	#print dir(homeUrl)
	
	homeHref = homeUrl.get_attribute("href")
	print "home ref on 404 page: ", homeHref
	
	driver.get(homeHref)

	print sys.argv[0], "PASSED"
	driver.close()
	
except Exception as e:
	if debugMode: driver.close()
	print "Test failed: ", e
	traceback.print_exc(1)
    