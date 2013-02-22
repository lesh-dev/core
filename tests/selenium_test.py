#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import random, traceback, sys
from datetime import datetime
import time

from bawlib import isVoid, isList, isString, isEqual, getSingleOption, userSerialize, toUnicode

#['_unwrap_value', '_wrap_value', 'add_cookie',
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

class TestError(RuntimeError):
	pass

class TestFatal(TestError):
	pass

class ItemNotFound(TestError):
	pass

class TestShutdown(RuntimeError):
	pass

class TestAction:
	def __init__(self, action, details):
		self.m_action = action
		self.m_details = details
		
	def printAction(self):
		print toUnicode(self.m_action + " " + self.m_details)

# generic function to run any test.
def RunTest(test):
	try:
		test.init()
		test.run()
	except TestFatal as e:
#		test.printActionLog()
		test.handleTestFatal(e)
	except TestError as e:
		print "Test action log:"
		test.printActionLog()
		test.handleTestFail(e)
	except TestShutdown as e:
		test.handleShutdown(e)
	except Exception as e:
		test.handleException(e)
	
#main API wrapper for Webdriver.
class SeleniumTest:
	def __init__(self, baseUrl, params = []):
#		print "Init SeleniumTest"
		self.m_testName = self.__class__.__name__
		self.m_baseUrl = baseUrl
		self.m_params = params

		self.initDefaults()
		
		if self.needDoc():
			print self.m_testName, "test info:"
			print self.getDoc()
			raise TestShutdown("Display doc")
			
		if self.needLeaveBrowserOpen():
			self.setCloseOnExit(False)
	
		
		
#		self.m_driver.window_maximize()
	
	def initDefaults(self):
		self.m_checkErrors = True
		self.m_closeOnExit = True
		self.m_logStarted = False
		self.m_errorsAsWarnings = False
		
		self.m_logFile = self.m_testName + ".log" #"_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") +
		self.m_actionLog = []
		
	def init(self):
		self.m_baseUrl = self.fixBaseUrl(self.getBaseUrl())
		self.m_driver = webdriver.Firefox()
	
	def getName(self):
		return self.m_testName
		
	def getDoc(self):
		return self.__doc__
	
	def maximizeWindow(self):
		if hasattr(self, 'm_driver'):
			self.m_driver.maximize_window()		
			
	def __del__(self):
#		print "Destructing SeleniumTest"
		if hasattr(self, 'm_driver'):
			if self.m_closeOnExit:
#				print "closing driver"
				self.m_driver.close()

	def getBaseUrl(self):
		if isVoid(self.m_baseUrl):
			self.failTest("Base URL for test '" + self.getName() + "' is not set. ")
		return self.m_baseUrl
	
	def needDoc(self):
		opt, _ = getSingleOption(["-d", "--doc"], self.m_params)
		return opt
		
	def needLeaveBrowserOpen(self):
		opt, _ = getSingleOption(["-p", "--preserve"], self.m_params);
		return opt
			
	def shutdown(self, exitCode = 0):
		sys.exit(exitCode)
		
	def handleShutdown(self, exc):
		self.shutdown(0)
		
	def handleException(self, exc):
		print "TEST ERROR:", toUnicode(exc.message)
		traceback.print_exc()
		self.shutdown(2)
				
	def handleTestFail(self, exc):
		print "TEST FAILED:", toUnicode(exc.message)
		self.shutdown(1)

	def handleTestFatal(self, exc):
		print "TEST FATALED:", toUnicode(exc.message)
		self.shutdown(2)

	def getActionLog(self):
		# return copy of navigation log
		return self.m_actionLog[:]
	
	def printActionLog(self):
		for act in self.m_actionLog:
			act.printAction()
		
	def logStart(self):
		try:
			logFile = open(self.m_logFile, "w")
			logText = "[" + self.m_testName + " log start]\n"
			logFile.write(toUnicode(logText))
			logFile.close()
			#indicate that log was already created
			self.m_logStarted = True
		except IOError:
			raise RuntimeError("Cannot create log file '" + m_logFile + "'. ")
			
	def setCloseOnExit(self, flag):
		self.m_closeOnExit = flag;
		
	# PHP errors auto-check toggle
	def setAutoPhpErrorChecking(self, checkErrors = True):
		self.m_checkErrors = checkErrors

	def setPhpErrorsAsWarnings(self, errorsAsWarnings = True):
		self.m_errorsAsWarnings = errorsAsWarnings
	
	def fixBaseUrl(self, url):
		if not (url.startswith("http://") or url.startswith("https://")):
			url = "http://" + url;
		return url;

	# get current URL of tested site
	def curUrl(self):
		return self.m_driver.current_url;
	
	def gotoRoot(self):
		return self.gotoPage("/")
		
	def gotoPage(self, url):
		fullUrl = self.m_baseUrl + url
		return self.gotoSite(fullUrl)
	
	def gotoSite(self, fullUrl):
		self.addAction("navigate", fullUrl)
		self.m_driver.get(fullUrl)
		if self.m_checkErrors:
			self.assertPhpErrors();
			
	def gotoUrlByLinkText(self, linkName):
		try:
			link = self.getUrlByLinkText(linkName)
			self.gotoSite(link)
		except NoSuchElementException:
			self.failTest(u"Cannot find URL with name '" + userSerialize(linkName) + "'. ")

	def displayReason(self, reason):
		if reason is None or reason == "":
			return ""
		else:
			return "Reason: '" + reason + "'. "

	def assertUrlNotPresent(self, linkName, forbidReason = ""):
		try:
			self.getUrlByLinkText(linkName)
			exceptionMessage = "Forbidden URL is found on the page in assertUrlNotPresent: '" + userSerialize(linkName) + "'. " + self.displayReason(forbidReason)
			raise TestError(exceptionMessage)
		except ItemNotFound:
			pass
	
	def drv(self):
		return self.m_driver;

	def getElementByName(self, name):
		try:
			return self.m_driver.find_element_by_name(name)
		except NoSuchElementException:
			self.logAdd("getElementByName failed for name '" + name + "':\n" + traceback.format_exc())
			raise TestError(u"Cannot get element by name '" + name + "'. ")

	def getElementById(self, eleId):
		try:
			return self.m_driver.find_element_by_id(eleId)
		except NoSuchElementException:
			self.logAdd("getElementById failed for name '" + name + "':\n" + traceback.format_exc())
			raise TestError(u"Cannot get element by name '" + name + "'. ")
			
	def fillElementByName(self, name, text):
		self.checkEmptyParam(name, "fillElementByName")
		self.addAction("fill", "element name: '" + name + "', text: '" + text + "'")
		self.getElementByName(name).send_keys(text)
		return self.getElementByName(name).get_attribute('value')
		
	def fillElementById(self, eleId, text):
		self.checkEmptyParam(eleId, "fillElementById")
		self.addAction("fill", "element id: '" + eleId + "', text: '" + text + "'")
		self.getElementById(eleId).send_keys(text)
		return self.getElementById(eleId).get_attribute('value')

	def getElementValueById(self, eleId):
		self.checkEmptyParam(eleId, "getElementValueById")
		self.addAction("get-value", "element id: '" + eleId + "'")
		return self.getElementById(eleId).get_attribute('value')

	def getElementValueByName(self, eleName):
		self.checkEmptyParam(eleName, "getElementValueByName")
		self.addAction("get-value", "element name: '" + eleName + "'")
		return self.getElementByName(eleName).get_attribute('value')

	def checkElementValueById(self, eleId, text):
		self.checkEmptyParam(eleId, "checkElementValueById")
		self.addAction("check-value", "element id: '" + eleId + "'")
		eleValue = self.getElementById(eleId).get_attribute('value')
		if isEqual(eleValue, text):
			return True
		return False

	def assertElementValueById(self, eleId, text):
		if not self.checkElementValueById(eleId, text):
			raise TestError("Element '" + eleId + "' value does not match expected: '" + text + "'. ")

	def addAction(self, name, details = ""):
		self.m_actionLog.append(TestAction(name, details))		
	
	def clickElementByName(self, name):
		self.addAction("click", "element name: '" + name + "'")
		self.getElementByName(name).click()

	def clickElementById(self, eleId):
		self.addAction("click", "element id: '" + eleId + "'")
		self.getElementById(eleId).click()
	
	def getElementContent(self, xpath):
		return self.m_driver.find_element_by_xpath(xpath).text
		
	def checkTextPresent(self, xpath, text):
		self.checkEmptyParam(xpath, "checkTextPresent")
		self.checkEmptyParam(text, "checkTextPresent")
		
		count = 0
		while count < 3:
			try:
				if isList(text):
					for phrase in text:
						if phrase in self.m_driver.find_element_by_xpath(xpath).text:
							return True
					return False
				else:
					return text in self.m_driver.find_element_by_xpath(xpath).text
			except NoSuchElementException:
				#self.logAdd("checkTextPresent does not found xpath '" + xpath + "':\n" + traceback.format_exc())
				return False
			except StaleElementReferenceException:
				self.logAdd("Cache problem in checkTextPresent(" + xpath + ", " + userSerialize(text) + "), trying again. ")
				count += 1
				time.sleep(1)
				continue
		self.failTest("Unsolvable cache problem in checkTextPresent(" + xpath + ", " + userSerialize(text) + "), trying again. ")
		
	def checkSourceTextPresent(self, text):
		return self.checkTextPresent("//*", text)
		
	def checkBodyTextPresent(self, text):
		return self.checkTextPresent("/html/body", text)
		
	def failTest(self, errorText):
		self.logAdd(errorText)
		raise TestError(errorText)

	def failTestWithItemNotFound(self, errorText):
		self.logAdd(errorText)
		raise ItemNotFound(errorText)

	def assertTextPresent(self, xpath, text):
		if not self.checkTextPresent(xpath, text):
			self.failTest("Text '" + userSerialize(text) + "' not found on page '" + self.curUrl() + "' in element '" + xpath + "'. ")

	def assertTextNotPresent(self, xpath, text, forbidReason = ""):
		if self.checkTextPresent(xpath, text):
			errText = "Forbidden text '" + userSerialize(text) + "' found on page '" + self.curUrl() + "' in element '" + xpath + "'. " + self.displayReason(forbidReason)
			self.failTest(errText)

	def assertBodyTextPresent(self, text):
		return self.assertTextPresent("/html/body", text)

	def assertBodyTextNotPresent(self, text, forbidReason = ""):
		return self.assertTextNotPresent("/html/body", text, forbidReason)

	def assertSourceTextPresent(self, text):
		return self.assertTextPresent("//*", text)

	def assertSourceTextNotPresent(self, text):
		return self.assertTextNotPresent("//*", text)

	def checkEmptyParam(self, stringOrList, methodName):
		if isList(stringOrList):
			if len(stringOrList) == 0:
				raise RuntimeError("Empty list passed to " + methodName);
			for text in stringOrList:
				if isVoid(text):
					raise RuntimeError("Empty string passed in the list to " + methodName);
		else:		
			if isVoid(stringOrList):
				raise RuntimeError("Empty param passed to " + methodName);

	def getUrlByLinkText(self, urlText):
		self.checkEmptyParam(urlText, "getUrlByLinkText");
		if isList(urlText):
			for urlName in urlText:
				try:
					url = self.m_driver.find_element_by_link_text(urlName)
					return url.get_attribute("href");
				except NoSuchElementException:
					self.logAdd("Tried to find url by name '" + urlName + "', not found. ")
					pass
			else:
				# loop ended, found nothing
				# here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
				msg = u"Cannot find URL by link texts: '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. "
				self.failTestWithItemNotFound(msg)
		else:		
			try:
				url = self.m_driver.find_element_by_link_text(urlText)
				return url.get_attribute("href");
			except NoSuchElementException:
				# here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
				msg = u"Cannot find URL by link text: '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. "
				self.failTestWithItemNotFound(msg)
			
	def logAdd(self, text):
		try:
			if not self.m_logStarted:
				self.logStart()
				
			logFile = open(self.m_logFile, 'a')
			fullLogText = text + u"\n"
			logFile.write(fullLogText.encode('UTF-8'))
			logFile.close()
		except IOError:
			raise RuntimeError("Cannot write message to log file '" + m_logFile + "'. ")
		
	
	def getPageSource(self):
		return self.m_driver.page_source;
		
	def checkPhpErrors(self):
		#print dir(self.m_driver);
		pageText = self.m_driver.page_source
		susp = ["Notice:", "Error:", "Warning:", "Fatal error:", "Parse error:"];
		for word in susp:
			if (word in pageText) and (" on line " in pageText):
				self.logAdd("PHP ERROR '" + word + "' detected on page '" + self.curUrl() + "':")
				self.logAdd("ERROR_PAGE_BEGIN =================")
				self.logAdd(pageText)
				self.logAdd("ERROR_PAGE_END ===================")
				return True, word
		return False, None
	
	def assertPhpErrors(self):
		checkResult, suspWord = self.checkPhpErrors()
		if checkResult:
			logMsg = "PHP error '" + suspWord + "' detected on the page '" + self.curUrl() + "'"
			self.logAdd(logMsg)
			if not self.m_errorsAsWarnings:
				raise TestError(logMsg)
	

