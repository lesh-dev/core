#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException

from urllib2 import URLError
from httplib import HTTPException

from selenium.webdriver.remote.webdriver import WebElement

import random, traceback, sys
from datetime import datetime
import time

from bawlib import isVoid, isList, isString, isEqual, getSingleOption, userSerialize, toUnicode

#['_unwrap_value', '_wrap_value', 'add_cookie',
#'back', 'binary', 'capabilities', 'close', 'command_executor', 'create_web_element', 'current_window_handle',
#'delete_all_cookies', 'delete_cookie', 'desired_capabilities', 'error_handler', 'execute', 'execute_async_script',
#'execute_script', 'find_element', 'find_element_by_class_name', 'find_element_by_css_selector', 
# 'find_element_by_partial_link_text', 'find_element_by_tag_name',
#'find_element_by_xpath', 'find_elements', 'find_elements_by_class_name', 'find_elements_by_css_selector', 'find_elements_by_id',
#'find_elements_by_link_text', 'find_elements_by_name', 'find_elements_by_partial_link_text', 'find_elements_by_tag_name',
#'find_elements_by_xpath', 'firefox_profile', 'forward', 'get', 'get_cookie', 'get_cookies', 'get_screenshot_as_base64',
#'get_screenshot_as_file', 'get_window_position', 'get_window_size', 'implicitly_wait', 
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
        return 0
    except TestFatal as e:
#       test.printActionLog()
        test.handleTestFatal(e)
        return 2
    except TestError as e:
        test.handleTestFail(e)
        print "Test " + test.getName() + " action log:"
        test.printActionLog()
        return 1
    except TestShutdown as e:
        test.handleShutdown(e)
        return 0
    except NoSuchWindowException as e:
        print "Seems like browser window have been closed. "
        return 2
    except URLError as e:
        print "URL error occured. Seems like browser connection error occured (window has been closed, etc). "
        return 2
    except HTTPException as e:
        print "HTTP error occured. Seems like browser connection error occured (window has been closed, etc). "
        return 2
    except Exception as e:
        test.handleException(e)
        return 2
        
def DecodeRunResult(result):
    if result == 0: return "PASSED"
    elif result == 1: return "FAILED"
    elif result == 2: return "FATAL"
    else: return "UNKNOWN"
    
def getValue(ele):
    return ele.get_attribute('value')
    
#main API wrapper for Webdriver.
class SeleniumTest:
    def __init__(self, baseUrl, params = []):
#       print "Init SeleniumTest"
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
        
        
#       self.m_driver.window_maximize()
    
    def initDefaults(self):
        self.m_checkErrors = True
        self.m_closeOnExit = True
        self.m_logStarted = False
        self.m_errorsAsWarnings = False
        
        self.m_logFile = self.m_testName + ".log" #"_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") +
        self.m_actionLog = []
        
    def init(self):
        self.m_baseUrl = self.fixBaseUrl(self.getBaseUrl())
        self.m_driver = webdriver.Firefox() #executable_path="/usr/bin/firefox")
        self.maximizeWindow()
    
    def getName(self):
        return self.m_testName
        
    def getDoc(self):
        return self.__doc__
    
    def maximizeWindow(self):
        if hasattr(self, 'm_driver'):
            self.m_driver.maximize_window()     
            
    def __del__(self):
#        print "Destructing SeleniumTest"
        if hasattr(self, 'm_driver'):
            if self.m_closeOnExit:
#                print "Closing driver"
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
        print "TEST " + self.getName() + " ERROR:", toUnicode(exc.message)
        traceback.print_exc()
        self.shutdown(2)
                
    def handleTestFail(self, exc):
        #self.m_driver.execute_script("alert('Test failed! See console log for details. ');")
        print "TEST " + self.getName() + " FAILED:", toUnicode(exc.message)
        self.shutdown(1)

    def handleTestFatal(self, exc):
        #self.m_driver.execute_script("alert('Test fataled! See logs and check your test/environment. ');")
        print "TEST " + self.getName() + " FATALED:", toUnicode(exc.message)
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
            logText = "[" + self.m_testName + " log start on " + self.m_baseUrl + "]\n"
            logFile.write(toUnicode(logText))
            logFile.close()
            #indicate that log was already created
            self.m_logStarted = True
        except IOError:
            raise RuntimeError("Cannot create log file '" + self.m_logFile + "'. ")
            
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
        
    # @comment usually means link name (or id), which we used to navigate to this URL.
    def gotoPage(self, url, comment = ""):
        fullUrl = self.m_baseUrl + url
        return self.gotoSite(fullUrl, comment)
    
    # @comment usually means link name (or id), which we used to navigate to this URL.
    def gotoSite(self, fullUrl, comment = ""):
        actionMsg = u"Link: '" + userSerialize(fullUrl);
        if not isVoid(comment):
            actionMsg +=  (u"' comment: '" + userSerialize(comment) + "'")
        self.addAction("navigate", actionMsg)
        self.m_driver.get(fullUrl)
        if self.m_checkErrors:
            self.assertPhpErrors();
            
    def gotoUrlByLinkText(self, linkName):
        try:
            link = self.getUrlByLinkText(linkName)
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest(u"Cannot find URL with name '" + userSerialize(linkName) + "'. ")

    def gotoUrlByPartialLinkText(self, linkName):
        try:
            link = self.getUrlByLinkText(linkName, ["partial"])
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest(u"Cannot find URL with name '" + userSerialize(linkName) + "'. ")

    def gotoUrlByLinkId(self, linkId):
        href = self.getElementById(linkId).get_attribute("href")
        self.gotoSite(href, linkId)

    def getImageSrcById(self, imageId):
        return self.getElementById(imageId).get_attribute("src")

    def displayReason(self, reason):
        if isVoid(reason):
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

    def assertUrlPresent(self, linkName, reason = ""):
        try:
            self.getUrlByLinkText(linkName)
        except ItemNotFound:
            exceptionMessage = "Required URL is not found on the page in assertUrlPresent: '" + userSerialize(linkName) + "'. " + self.displayReason(reason)
            raise TestError(exceptionMessage)

    def wait(self, seconds):
        self.logAdd("Waiting for " + userSerialize(seconds) + "' seconds. ")
        time.sleep(seconds)
        
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
            self.logAdd("getElementById failed for id '" + eleId + "':\n" + traceback.format_exc())
            raise TestError(u"Cannot get element by id '" + eleId + "'. ")
        
    def checkboxIsValid(self, value):
        return value == "checked" or value == "true"
                
    def checkCheckboxValueById(self, eleId, boolValue = True):
        self.checkEmptyParam(eleId, "checkCheckboxValueById")
        value = self.getElementById(eleId).get_attribute("checked")
#       print "value: ", value
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox '" + eleId + "': " + userSerialize(value)
            self.logAdd(msg)
            raise TestError(msg)
        
        if boolValue: # check if it is 'checked'
            if value and self.checkboxIsValid(value):
                return True
            return False
        else: # check if it is unchecked
            if value and self.checkboxIsValid(value):
                return False
            return True
                
    def assertCheckboxValueById(self, eleId, boolValue = True):
        if not self.checkCheckboxValueById(eleId, boolValue):
            raise TestError(u"Checkbox with id '" + eleId + "' has improper value, expected '" + userSerialize(boolValue) + "'. ")
            
    def fillElementByName(self, name, text, clear = True):
        self.checkEmptyParam(name, "fillElementByName")
        if clear:
            self.addAction("clear", "element name: '" + name + "'")
            self.getElementByName(name).clear()
        self.addAction("fill", "element name: '" + name + "', text: '" + text + "'")
        self.getElementByName(name).send_keys(text)
        return getValue(self.getElementByName(name))
        
    def fillElementById(self, eleId, text, clear = True):
        try:
            self.checkEmptyParam(eleId, "fillElementById")
            if clear:
                self.addAction("clear", "element id: '" + eleId + "'")
                self.getElementById(eleId).clear()

            self.addAction("fill", "element id: '" + eleId + "', text: '" + text + "'")
            #print "sending keys" , text
            ele = self.getElementById(eleId)
            #print "got element "
            #print "dir", dir(ele)
            ele.send_keys(text)
            return getValue(self.getElementById(eleId))
        except InvalidElementStateException as e:
            self.logAdd("fillElementById failed for id '" + eleId + "':\n" + traceback.format_exc())
            raise TestError(u"Cannot set element value by id '" + eleId + "', possibly element is read-only.")
            
    
    def setOptionValueById(self, eleId, optValue):
        try:
            self.getElementById(eleId).find_element_by_xpath(u"//option[@value='" + optValue + "']").click()
        except NoSuchElementException:
            self.logAdd("setOptionValueById failed for id '" + eleId + "':\n" + traceback.format_exc())
            raise TestError(u"Cannot get drop-down (select) element by id '" + eleId + "'. ")

    def getOptionValueByName(self, eleName):
        try:
            return getValue(self.getElementByName(eleName).find_element_by_xpath("//option[@selected='selected']"))
        except NoSuchElementException:
            self.logAdd("getOptionValueByName failed for name '" + eleName + "':\n" + traceback.format_exc())
            raise TestError(u"Cannot get drop-down (select) element by name '" + eleName + "'. ")
        
    def getOptionValueById(self, eleId):
        try:
            return getValue(self.getElementById(eleId).find_element_by_xpath(u"//option[@selected='selected']"))
        except NoSuchElementException:
            self.logAdd("getOptionValueById failed for id '" + eleId + "':\n" + traceback.format_exc())
            raise TestError(u"Cannot get drop-down (select) element by id '" + eleId + "'. ")

    def getElementValueById(self, eleId):
        self.checkEmptyParam(eleId, "getElementValueById")
        self.addAction("get-value", "element id: '" + eleId + "'")
        return getValue(self.getElementById(eleId))

    def getElementValueByName(self, eleName):
        self.checkEmptyParam(eleName, "getElementValueByName")
        self.addAction("get-value", "element name: '" + eleName + "'")
        return getValue(self.getElementByName(eleName))

    def checkElementValueById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementValueById")
        self.addAction("check-value", "element id: '" + eleId + "', expected: '" + text + "'. ")
        eleValue = getValue(self.getElementById(eleId))
        if isEqual(eleValue, text):
            return True
        return False

    def checkElementTextById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementTextById")
        self.addAction("check-text", "element id: '" + eleId + "', expected: '" + text + "'. ")
        eleText = self.getElementById(eleId).text
        if isEqual(eleText, text):
            return True
        return False

    def checkElementValueByName(self, name, text):
        self.checkEmptyParam(name, "checkElementValueByName")
        self.addAction("check-value", "element name: '" + name + "', expected: '" + text + "'. ")
        eleValue = getValue(self.getElementByName(name))
        if isEqual(eleValue, text):
            return True
        return False

    def assertElementTextById(self, eleId, text):
        if not self.checkElementTextById(eleId, text):
            raise TestError("Element with id '" + eleId + "' text does not match expected: '" + text + "'. ")

    def assertElementValueById(self, eleId, text):
        if not self.checkElementValueById(eleId, text):
            raise TestError("Element with id '" + eleId + "' value does not match expected: '" + text + "'. ")

    def assertElementValueByName(self, name, text):
        if not self.checkElementValueByName(name, text):
            raise TestError("Element with name '" + name + "' value does not match expected: '" + text + "'. ")

    def addAction(self, name, details = ""):
        self.m_actionLog.append(TestAction(name, details))      
    
    def clickElementByName(self, name):
        self.addAction("click", "element name: '" + name + "'")
        self.getElementByName(name).click()
        if self.m_checkErrors:
            self.assertPhpErrors();

    def clickElementById(self, eleId):
        self.addAction("click", "element id: '" + eleId + "'")
        self.getElementById(eleId).click()
        if self.m_checkErrors:
            self.assertPhpErrors();
    
    # getElementText
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
                self.wait(1.0)
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

    def assertTextPresent(self, xpath, text, reason = ""):
        if not self.checkTextPresent(xpath, text):
            self.failTest("Text '" + userSerialize(text) + "' not found on page '" + self.curUrl() + "' in element '" + xpath + "'. " + self.displayReason(reason))

    def assertTextNotPresent(self, xpath, text, forbidReason = ""):
        if self.checkTextPresent(xpath, text):
            errText = "Forbidden text '" + userSerialize(text) + "' found on page '" + self.curUrl() + "' in element '" + xpath + "'. " + self.displayReason(forbidReason)
            self.failTest(errText)

    def assertBodyTextPresent(self, text, reason = ""):
        return self.assertTextPresent("/html/body", text, reason)

    def assertBodyTextNotPresent(self, text, forbidReason = ""):
        return self.assertTextNotPresent("/html/body", text, forbidReason)

    def assertSourceTextPresent(self, text):
        return self.assertTextPresent("//*", text)

    def assertSourceTextNotPresent(self, text, forbidReason = ""):
        return self.assertTextNotPresent("//*", text, forbidReason)

    def checkEmptyParam(self, stringOrList, methodName):
        if isList(stringOrList):
            if len(stringOrList) == 0:
                raise RuntimeError("Empty list passed to " + methodName)
            for text in stringOrList:
                if isVoid(text):
                    raise RuntimeError("Empty string passed in the list to " + methodName)
        else:       
            if isVoid(stringOrList):
                raise RuntimeError("Empty param passed to " + methodName)

    def getUrlByLinkText(self, urlText, optionList = []):
        self.checkEmptyParam(urlText, "getUrlByLinkText");
        searchMethod = self.m_driver.find_element_by_link_text
        if "partial" in optionList:
            self.logAdd(u"Search for partial link text '" + userSerialize(urlText) + "'. ")
            searchMethod = self.m_driver.find_element_by_partial_link_text
        
        if isList(urlText):
            for urlName in urlText:
                try:
                    url = searchMethod(urlName)
                    return url.get_attribute("href");
                except NoSuchElementException:
                    self.logAdd("Tried to find url by name '" + urlName + "', not found. ")
                    pass
            else:
                # loop ended, found nothing
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = u"Cannot find URL by link texts: '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. "
                self.failTestWithItemNotFound(msg)
        else: # single link
            try:
                url = searchMethod(urlText)
                return url.get_attribute("href");
            except NoSuchElementException:
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = u"Cannot find URL by link text: '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. "
                self.failTestWithItemNotFound(msg)

    def gotoIndexedUrlByLinkText(self, urlText, index):
        try:
            urls = self.m_driver.find_elements_by_xpath("//a[text()='" + urlText + "']")

            #print "Type = ", type(urls)
            if isList(urls):
                if index < len(urls):
                    url = urls[index]
                    href = url.get_attribute("href")
                    self.logAdd("Found URL with index " + userSerialize(index) + ": " + href)
                    self.gotoSite(href)
                else:
                    self.failTest(u"No index in URL array with link text '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. ")
            else:
                raise RuntimeError("Something bad retrieved from find_elements_by_xpath: it's not a list of WebElement. ")
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = u"Cannot find no one URL by link text: '" + userSerialize(urlText) + "' on page '" + self.curUrl() + "'. "
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
    

