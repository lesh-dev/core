#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import random, traceback, sys
from datetime import datetime

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

def isList(x):
	return type(x) == type(list())
	
class TestError(RuntimeError):
	pass

class TestShutdown(RuntimeError):
	pass

class TestAction:
	def __init__(self, action, details):
		self.m_action = action
		self.m_details = details
		
	def printAction(self):
		print unicode(self.m_action + " " + self.m_details).encode("utf-8")

# generic function to run any test.
def RunTest(test):
	try:
		test.init()
		test.run()
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
	def __init__(self):
#		print "Init SeleniumTest"
		self.m_testName = self.__class__.__name__

		self.initDefaults()
		
		if self.needHelp():
			print self.m_testName, "test info:"
			print self.getDoc()
			raise TestShutdown("Display help")
			
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
		
		#
	def getDoc(self):
		return self.__doc__
			
	def __del__(self):
#		print "Destructing SeleniumTest"
		if hasattr(self, 'm_driver'):
			if self.m_closeOnExit:
#				print "closing driver"
				self.m_driver.close()

	def getBaseUrl(self):
		if len(sys.argv) < 2:
			raise TestError("Base URL for test is not set. ")
		return sys.argv[1]
	
	def needHelp(self):
		"""
		called to detemine wether help is needed.
		uses sys.argv by default (keys --help or -h)
		"""
		return "--help" in sys.argv or "-h" in sys.argv
		
	def needLeaveBrowserOpen(self):
		return "-l" in sys.argv or "--leave-open" in sys.argv
			
	def shutdown(self, exitCode = 0):
		sys.exit(exitCode)
		
	def handleShutdown(self, exc):
		self.shutdown(0)
		
	def handleException(self, exc):
		print "TEST ERROR:", unicode(exc.message).encode("utf-8")
		traceback.print_exc()
		self.shutdown(2)
				
	def handleTestFail(self, exc):
		print "TEST FAILED:", unicode(exc.message).encode("utf-8")
		self.shutdown(1)
	
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
			logFile.write(logText.encode("utf-8"))
			logFile.close()
			#indicate that log was already created
			self.m_logStarted = True
		except IOError:
			raise RuntimeError("Cannot create log file '" + m_logFile + "'. ")
		
	def isVoid(self, text):
		return text is None or text.strip() == "";
	
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
			self.logAdd("gotoUrlLinkByText failed for link name '" + linkName + "':\n" + traceback.format_exc())
			raise TestError(u"Cannot find URL with name '" + linkName + "'")
		
	def assertUrlNotPresent(self, linkName):
		try:
			self.getUrlByLinkText(linkName)
			raise TestError("Forbidden URL is found on the page in assertUrlNotPresent: '" + linkName + "'")
		except TestError:
			pass
	
	def drv(self):
		return self.m_driver;

	def getElementByName(self, name):
		try:
			return self.m_driver.find_element_by_name(name)
		except NoSuchElementException:
			self.logAdd("getElementByName failed for name '" + name + "':\n" + traceback.format_exc())
			raise TestError(u"Cannot get element by name '" + name + "'")

	def getElementById(self, eleId):
		try:
			return self.m_driver.find_element_by_id(eleId)
		except NoSuchElementException:
			self.logAdd("getElementById failed for name '" + name + "':\n" + traceback.format_exc())
			raise TestError(u"Cannot get element by name '" + name + "'")
			
	def fillElementByName(self, name, text):
		if self.isVoid(name):
			raise RuntimeError("Empty element name passed to fillElementByName(). ")
		self.addAction("fill", "element name: '" + name + "', text: '" + text + "'")
		self.getElementByName(name).send_keys(text)
		return self.getElementByName(name).get_attribute('value')
		
	def fillElementById(self, eleId, text):
		if self.isVoid(eleId):
			raise RuntimeError("Empty element ID passed to fillElementById(). ")
		self.addAction("fill", "element id: '" + eleId + "', text: '" + text + "'")
		self.getElementById(eleId).send_keys(text)
		return self.getElementById(eleId).get_attribute('value')

	def addAction(self, name, details):
		self.m_actionLog.append(TestAction(name, details))		
	
	def clickElementByName(self, name):
		self.addAction("click", "element name: '" + name + "'")
		self.getElementByName(name).click()

	def clickElementById(self, eleId):
		self.addAction("click", "element id: '" + eleId + "'")
		self.getElementById(eleId).click()
	
	def checkTextPresent(self, xpath, text):
		if self.isVoid(xpath):
			raise RuntimeError("Empty XPath passed to checkTextPresent");
		
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
		
	def checkSourceTextPresent(self, text):
		return self.checkTextPresent("//*", text)
		
	def checkBodyTextPresent(self, text):
		return self.checkTextPresent("/html/body", text)
		
	def failTest(self, errorText):
		self.logAdd(errorText)
		raise TestError(errorText)
		
	def assertTextPresent(self, xpath, text):
		if not self.checkTextPresent(xpath, text):
			textInError = text
			if isList(text):
				textInError = text.join("|")
			self.failTest("Text '" + textInError + "' not found on page '" + self.curUrl() + "' in element '" + xpath + "'")

	def assertBodyTextPresent(self, text):
		return self.assertTextPresent("/html/body", text)
	
	def assertSourceTextPresent(self, text):
		return self.assertTextPresent("//*", text)
			
	def getUrlByLinkText(self, urlText):
		if self.isVoid(urlText):
			raise RuntimeError("Empty URL text passed to getUrlByLinkText");
		try:
			url = self.m_driver.find_element_by_link_text(urlText)
			return url.get_attribute("href");
		except NoSuchElementException:
			self.failTest(u"Cannot find URL by link text: '" + urlText + "' on page '" + self.curUrl())
			
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
	

