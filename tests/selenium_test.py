#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import sys, random

#['NATIVE_EVENTS_ALLOWED', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__',
#'__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
#'__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_unwrap_value', '_wrap_value', 'add_cookie',
#'back', 'binary', 'capabilities', 'close', 'command_executor', 'create_web_element', 'current_url', 'current_window_handle',
#'delete_all_cookies', 'delete_cookie', 'desired_capabilities', 'error_handler', 'execute', 'execute_async_script',
#'execute_script', 'find_element', 'find_element_by_class_name', 'find_element_by_css_selector', 'find_element_by_id',
#'find_element_by_link_text', 'find_element_by_name', 'find_element_by_partial_link_text', 'find_element_by_tag_name',
#'find_element_by_xpath', 'find_elements', 'find_elements_by_class_name', 'find_elements_by_css_selector', 'find_elements_by_id',
#'find_elements_by_link_text', 'find_elements_by_name', 'find_elements_by_partial_link_text', 'find_elements_by_tag_name',
#'find_elements_by_xpath', 'firefox_profile', 'forward', 'get', 'get_cookie', 'get_cookies', 'get_screenshot_as_base64',
#'get_screenshot_as_file', 'get_window_position', 'get_window_size', 'implicitly_wait', 'maximize_window',
#'name', 'orientation', 'page_source', 'profile', 'quit', 'refresh', 'save_screenshot', 'session_id',
#'set_page_load_timeout', 'set_script_timeout', 'set_window_position', 'set_window_size', 'start_client',
#'start_session', 'stop_client', 'switch_to_active_element', 'switch_to_alert', 'switch_to_default_content',
#'switch_to_frame', 'switch_to_window', 'title', 'window_handles']

rusAlphaSmall = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
rusAlphaCap = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
engAlphaSmall = "abcdefgiklmnopqrstuvwxyz"
engAlphaCap = "ABCDEFGHIKLMNOPQRSTUVWZYZ"

def randomText(length):
	rs = ""
	for i in range(0, length):
		rs = rs + random.choice('abcdef0123456789')
	return rs	

def randomWord(length):
	rs = ""
	
	enLang = (random.randint(0,10) < 7)
	
	if random.randint(0,10) < 3:
		if enLang:
			rs = random.choice(engAlphaCap)
		else:
			rs = random.choice(rusAlphaCap)
	else:
		if enLang:
			rs = random.choice(engAlphaSmall)
		else:
			rs = random.choice(rusAlphaSmall)
	
	for i in range(0, length):
		if enLang:
			rs = rs + random.choice(engAlphaSmall)
		else:
			rs = rs + random.choice(rusAlphaSmall)
		
	if random.choice(range(0,20)) < 3:
		rs = rs + random.choice('.,!?;:"<>-==@%$^&*()')
			
	return rs	
		
def randomDigits(length):
	rs = ""
	for i in range(0, length):
		rs = rs + str(random.choice('0123456789'))
	return rs

def randomCrap(wordNumber, multiLine = False):
	rs = ""
	for i in range(0, wordNumber):
		wordLen = random.randint(3,10)
		rs = rs + " " + randomWord(wordLen)
		if multiLine:
			if random.random() < 0.1:
				rs = rs + "\n"
	return rs

class SeleniumTest:
	def __init__(self, baseUrl = None):
#		print "Init SeleniumTest"
		self.m_checkErrors = False;
		self.m_closeOnExit = True;
		
		if baseUrl is None:
			if len(sys.argv) < 2:
				raise RuntimeError("Base URL for test is not set neither in class ctor, nor in CLI. ")
			else:
				baseUrl = sys.argv[1]
						
		self.m_driver = webdriver.Firefox()
		self.m_baseUrl = self.fixBaseUrl(baseUrl);
		
	def __del__(self):
#		print "Destructing SeleniumTest"
		if hasattr(self, 'm_driver'):
			if self.m_closeOnExit:
				self.m_driver.close()
				
	def isVoid(self, text):
		return text is None or text.strip() == "";
	
	def setCloseOnExit(self, flag):
		self.m_closeOnExit = flag;
		
	# PHP errors auto-check toggle
	def autoErrorCheckingOn(self):
		self.m_checkErrors = True;

	def autoErrorCheckingOff(self):
		self.m_checkErrors = False;
	
	def fixBaseUrl(self, url):
		if not (url.startswith("http://") or url.startswith("https://")):
			url = "http://" + url;
		return url;

	def curUrl(self):
		return self.m_driver.current_url;
	
	def gotoPage(self, url):
		fullUrl = self.m_baseUrl + url
			
		print "ST_DEBUG: navigating to " + fullUrl
		self.m_driver.get(fullUrl);
		if self.m_checkErrors:
			self.assertPhpErrors();
	
	def gotoSite(self, fullUrl):
		print "ST_DEBUG: Going to site " + fullUrl
		self.m_driver.get(fullUrl)
		if self.m_checkErrors:
			self.assertPhpErrors();
			
	def gotoUrlByLinkText(self, linkName):
		link = self.getUrlByLinkText(linkName)
		self.gotoSite(link)
			
	def drv(self):
		return self.m_driver;

	def getElementByName(self, name):
		return self.m_driver.find_element_by_name(name)

	def getElementById(self, eleId):
		return self.m_driver.find_element_by_id(eleId)

	def fillElementByName(self, name, text):
		if self.isVoid(name):
			raise RuntimeError("Empty element name passed to fillElementByName(). ")
		ele = self.getElementByName(name)
		ele.send_keys(text)

	def fillElementById(self, eleId, text):
		if self.isVoid(eleId):
			raise RuntimeError("Empty element ID passed to fillElementById(). ")
		ele = self.getElementById(eleId)
		ele.send_keys(text)
		return ele.get_attribute('value')

	def clickElementByName(self, name):
		butt = self.getElementByName(name)
		butt.click()

	def clickElementById(self, eleId):
		butt = self.getElementById(eleId)
		butt.click()
	
	def checkTextPresent(self, xpath, text):
		if self.isVoid(xpath):
			raise RuntimeError("Empty XPath passed to checkTextPresent");
		
		ele = self.m_driver.find_element_by_xpath(xpath)
		return text in ele.text;
		
	def assertTextPresent(self, xpath, text):
		if not self.checkTextPresent(xpath, text):
			raise RuntimeError("Text '" + text + "' not appers on page in element " + xpath)

	def assertBodyTextPresent(self, text):
		return self.assertTextPresent("/html/body", text)
	
	def assertSourceTextPresent(self, text):
		return self.assertTextPresent("//*", text)
			
	def getUrlByLinkText(self, urlText):
		if self.isVoid(urlText):
			raise RuntimeError("Empty URL text passed to getUrlByLinkText");
		
		url = self.m_driver.find_element_by_link_text(urlText)
		return url.get_attribute("href");
	
	def checkPhpErrors(self):
		#print dir(self.m_driver);
		pageText = self.m_driver.page_source
		susp = ["Notice:", "Error:", "Warning:", "Fatal error:", "Parse error:"];
		for word in susp:
			if (word in pageText) and (" on line " in pageText):
				return True
		return False
	
	def assertPhpErrors(self):
		if self.checkPhpErrors():
			raise RuntimeError("PHP errors detected on the page '" + self.curUrl() + "'")
	
		
		
		

