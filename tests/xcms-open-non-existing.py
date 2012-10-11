#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

debugMode = True #"TRUE" in os.getenv("XCMS_TEST_DEBUG");

class SeleniumTest:
	def __init__(self, baseUrl = None):
#		print "Init SeleniumTest"
		if baseUrl is None:
			if len(sys.argv) < 2:
				raise RuntimeError("Base URL for test is not set. ")
			else:
				baseUrl = sys.argv[1];
				
		self.m_driver = webdriver.Firefox()
		self.m_baseUrl = baseUrl;
		
	def __del__(self):
#		print "Destructing SeleniumTest"
		if hasattr(self, 'm_driver'):
			self.m_driver.close()
		
	def page(self, url):
		
		# detect if URL is full
		fullUrl = self.m_baseUrl + url
			
		print "Navigating to " + fullUrl
		self.m_driver.get(fullUrl);
	
	def site(self, fullUrl):
		print "Going to site " + fullUrl
		self.m_driver.get(fullUrl)
		
	def drv(self):
		return self.m_driver;
		
	def checkTextPresent(self, xpath, text):
		ele = self.m_driver.find_element_by_xpath(xpath)
		return text in ele.text;
		
	def assertTextPresent(self, xpath, text):
		if not self.checkTextPresent(xpath, text):
			raise RuntimeError("Text '" + text + "' not appers on page in element " + xpath)
			
	def getUrlByLinkText(self, urlText):
		url = self.m_driver.find_element_by_link_text(urlText)
		return url.get_attribute("href");
		
		

try:
	test = SeleniumTest()
	
	test.page("/qqq");
	
	test.assertTextPresent("//div[@class='error-widget']", u"Нет такой страницы")
	
	homeHref = test.getUrlByLinkText(u"этой ссылке")
	
	print "Home reference on 404 page: ", homeHref
	
	test.site(homeHref)
	
except Exception as e:
	#if debugMode: driver.close()
	print "TEST FAILED: ", e
	traceback.print_exc(1)
	sys.exit(1)
    