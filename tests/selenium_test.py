#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException

from urllib2 import URLError
from httplib import HTTPException

from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.ui import Select

import random, traceback, sys
from datetime import datetime
import time, os, shutil

from bawlib import isVoid, isList, isString, isNumber, isEqual, getSingleOption, userSerialize, wrapIfLong

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
        print self.m_action + " " + self.m_details

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
class SeleniumTest(object):
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
        if self.useChrome():
            chromePath = "/usr/bin/chromedriver"
            if not os.path.exists(chromePath):
                self.failTest("Chrome Driver is not installed. Please obtain latest version from\nhttp://chromedriver.storage.googleapis.com/index.html ")
            self.m_driver = webdriver.Chrome("/usr/bin/chromedriver")
        else:
            profileDir = "./test_profile"
            shutil.rmtree(profileDir, ignore_errors = True)
            os.mkdir(profileDir)
            fp = webdriver.FirefoxProfile(profileDir)
            self.m_driver = webdriver.Firefox(fp)
            
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
                self.m_driver.quit()

    def getBaseUrl(self):
        if isVoid(self.m_baseUrl):
            self.failTest("Base URL for test '" + self.getName() + "' is not set. ")
        return self.m_baseUrl
    
    def useChrome(self):
        chromeFlag, _ = getSingleOption(["-c", "--chrome"], self.m_params)
        return chromeFlag
    
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
        print "TEST " + self.getName() + " ERROR: " + userSerialize(exc.message)
        traceback.print_exc()
        self.shutdown(2)
                
    def handleTestFail(self, exc):
        #self.m_driver.execute_script("alert('Test failed! See console log for details. ');")
        print "TEST " + self.getName() + " FAILED: " + userSerialize(exc.message)
        self.shutdown(1)

    def handleTestFatal(self, exc):
        #self.m_driver.execute_script("alert('Test fataled! See logs and check your test/environment. ');")
        print "TEST " + self.getName() + " FATALED: " + userSerialize(exc.message)
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
            logFile.write(logText.encode("UTF-8"))
            logFile.close()
            #indicate that log was already created
            self.m_logStarted = True
        except IOError:
            raise RuntimeError("Cannot create log file " + userSerialize(self.m_logFile) + ". ")
            
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
        actionMsg = "Link: " + userSerialize(fullUrl);
        if not isVoid(comment):
            actionMsg +=  (" comment: " + userSerialize(comment) + " ")
        self.addAction("navigate", actionMsg)
        self.m_driver.get(fullUrl)
        
        self.checkPageErrors()

    def checkPageErrors(self):
        if self.m_checkErrors:
            self.assertPhpErrors()
            
    def gotoUrlByLinkText(self, linkName):
        try:
            link = self.getUrlByLinkText(linkName)
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest("Cannot find URL with name " + userSerialize(linkName) + ". ")

    def gotoUrlByPartialLinkText(self, linkName):
        try:
            link = self.getUrlByLinkText(linkName, ["partial"])
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest("Cannot find URL with name " + userSerialize(linkName) + ". ")

    def gotoUrlByLinkId(self, linkId):
        href = self.getElementById(linkId).get_attribute("href")
        self.gotoSite(href, linkId)

    def getImageSrcById(self, imageId):
        return self.getElementById(imageId).get_attribute("src")

    def displayReason(self, reason):
        if isVoid(reason):
            return ""
        else:
            return "Reason: " + userSerialize(reason) + ". "

    def assertUrlNotPresent(self, linkName, forbidReason = ""):
        try:
            self.getUrlByLinkText(linkName)
            exceptionMessage = "Forbidden URL is found on the page in assertUrlNotPresent: " + userSerialize(linkName) + ". " + self.displayReason(forbidReason)
            self.failTest(exceptionMessage)
        except ItemNotFound:
            pass

    def assertUrlPresent(self, linkName, reason = ""):
        try:
            self.getUrlByLinkText(linkName)
        except ItemNotFound:
            exceptionMessage = "Required URL is not found on the page in assertUrlPresent: " + userSerialize(linkName) + ". " + self.displayReason(reason)
            self.failTest(exceptionMessage)

    def wait(self, seconds):
        self.logAdd("Waiting for " + userSerialize(seconds) + " seconds. ")
        time.sleep(seconds)
        
    def drv(self):
        return self.m_driver;

    def getElementByName(self, name):
        try:
            return self.m_driver.find_element_by_name(name)
        except NoSuchElementException:
            self.failTest("Cannot get element by name " + userSerialize(name) + ". ")

    def getElementById(self, eleId):
        try:
            return self.m_driver.find_element_by_id(eleId)
        except NoSuchElementException:
            self.failTest("Cannot get element by id '" + eleId + "'. ")
        
    def checkboxIsValid(self, value):
        return value == "checked" or value == "true"
                
    def checkCheckboxValueById(self, eleId, boolValue = True):
        self.checkEmptyParam(eleId, "checkCheckboxValueById")
        value = self.getElementById(eleId).get_attribute("checked")
#       print "value: ", value
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox '" + eleId + "': " + userSerialize(value)
            self.failTest(msg)
        
        if boolValue: # check if it is 'checked'
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:true, element id: '" + eleId + "'. ")
                return True
            return False
        else: # check if it is unchecked
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:false, element id: '" + eleId + "'. ")
                return False
            return True
                
    def assertCheckboxValueById(self, eleId, boolValue = True):
        if not self.checkCheckboxValueById(eleId, boolValue):
            self.failTest("Checkbox with id '" + eleId + "' has improper value, expected " + userSerialize(boolValue) + ". ")
            
    def fillElementByName(self, name, text, clear = True):
        self.checkEmptyParam(name, "fillElementByName")
        if clear:
            self.addAction("clear", "element name: " + userSerialize(name) + " ")
            self.getElementByName(name).clear()
        self.addAction("fill", "element name: " + userSerialize(name) + ", text: " + wrapIfLong(userSerialize(text)) + " ")
        self.getElementByName(name).send_keys(text)
        return getValue(self.getElementByName(name))
        
    def fillElementById(self, eleId, text, clear = True):
        try:
            self.checkEmptyParam(eleId, "fillElementById")
            if clear:
                self.addAction("clear", "element id: '" + eleId + "'")
                self.getElementById(eleId).clear()

            self.addAction("fill", "element id: '" + eleId + "', text: " + wrapIfLong(userSerialize(text)) + " ")
            #print "sending keys" , text
            ele = self.getElementById(eleId)
            #print "got element "
            #print "dir", dir(ele)
            ele.send_keys(text)
            return getValue(self.getElementById(eleId))
        except InvalidElementStateException as e:
            self.failTest("Cannot set element value by id '" + eleId + "', possibly element is read-only.")
            
    def setOptionValueByIdAndValue(self, eleId, optValue):
        try:
            if isNumber(optValue):
                optValue = str(optValue)
            self.addAction("set-option-by-value", "element id: '" + eleId + "', value: " + userSerialize(optValue))
                
            self.getElementById(eleId).find_element_by_xpath("option[@value='" + optValue + "']").click()
            self.checkPageErrors()
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by id '" + eleId + "'. ")

    def setOptionValueByIdAndIndex(self, eleId, index):
        """
        element index is started with 1, not 0.
        """
        if index < 1:
            self.failTest("Invalid index in setOptionValueByIdAndIndex for element " + eleId + ". Index should be positive (1 and above). ")
        self.addAction("set-option-by-index", "element id: '" + eleId + "', index: " + userSerialize(index))
        selEle = self.getElementById(eleId)
        optionValue = getValue(selEle.find_element_by_xpath("option[" + userSerialize(index) + "]"))
        self.setOptionValueByIdAndValue(eleId, optionValue)

    def getOptionValueByName(self, eleName):
        try:
            return getValue(self.getElementByName(eleName).find_element_by_xpath("option[@selected='selected']"))
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by name " + userSerialize(eleName) + ". ")
        
    def getOptionValueById(self, eleId):
        try:
            return getValue(self.getElementById(eleId).find_element_by_xpath("option[@selected='selected']"))
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by id '" + eleId + "'. ")

    def getElementValueById(self, eleId):
        self.checkEmptyParam(eleId, "getElementValueById")
        self.addAction("get-value", "element id: '" + eleId + "'")
        return getValue(self.getElementById(eleId))

    def getElementValueByName(self, eleName):
        self.checkEmptyParam(eleName, "getElementValueByName")
        self.addAction("get-value", "element name: " + userSerialize(eleName) + " ")
        return getValue(self.getElementByName(eleName))

    def checkElementValueById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementValueById")
        self.addAction("check-value", "element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
        eleValue = getValue(self.getElementById(eleId))
        if not eleValue:
            self.logAdd("None 'value' in element id '" + eleId + "'. Maybe it has no attribute 'value'?", "warning")
            return False
        self.logAdd("checkElementValueById: current element '" + eleId + "' value is: " + wrapIfLong(userSerialize(eleValue)) + ". ")
        if isEqual(eleValue, text):
            self.logAdd("check-value:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.logAdd("check-value:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ", actual: " + wrapIfLong(userSerialize(eleValue)) + ". ")
        return False

    def checkElementTextById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementTextById")
        self.addAction("check-text", "element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
        eleText = self.getElementTextById(eleId)
        self.logAdd("checkElementTextById: current element '" + eleId + "', text is: " + wrapIfLong(userSerialize(eleText)) + ". ")
        if isEqual(eleText, text):
            self.logAdd("check-text:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.addAction("check-text:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ", actual: " + wrapIfLong(userSerialize(eleText)) + ". ")
        return False

    # checks if element eleId contains text 'text'.
    def checkElementSubTextById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementSubTextById")
        self.addAction("check-text", "element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
        eleText = self.getElementTextById(eleId)
        self.logAdd("checkElementSubTextById: current element '" + eleId + "', text is: " + wrapIfLong(userSerialize(eleText)) + ". ")
        if text in eleText:
            self.logAdd("check-subtext:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.addAction("check-subtext:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ", actual: " + wrapIfLong(userSerialize(eleText)) + ". ")
        return False

    def assertElementSubTextById(self, eleId, text):
        if not self.checkElementSubTextById(eleId, text):
            self.failTest("Element with id '" + eleId + "' text does not contain expected: " + wrapIfLong(userSerialize(text)) + ". ")

    def checkElementValueByName(self, name, text):
        self.checkEmptyParam(name, "checkElementValueByName")
        self.addAction("check-value", "element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
        eleValue = getValue(self.getElementByName(name))
        if not eleValue:
            self.logAdd("None 'value' in element named '" + name + "'. Maybe it has no attribute 'value'?", "warning")
            return False
        self.logAdd("checkElementValueByName: current element named '" + name + "' has value: " + wrapIfLong(userSerialize(eleValue)) + ". ")
        if isEqual(eleValue, text):
            self.logAdd("check-value:ok, element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.logAdd("check-value:fail, element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) + ", actual: " + wrapIfLong(userSerialize(eleText)) + ". ")
        return False

    def assertElementTextById(self, eleId, text, reason = ""):
        if not self.checkElementTextById(eleId, text):
            self.failTest("Element with id '" + eleId + "' text does not match expected: " + wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason))

    def assertElementValueById(self, eleId, text, reason = ""):
        if not self.checkElementValueById(eleId, text):
            self.failTest("Element with id '" + eleId + "' value does not match expected: " + wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason))

    def assertElementValueByName(self, name, text):
        if not self.checkElementValueByName(name, text):
            self.failTest("Element with name '" + userSerialize(name) + " value does not match expected: " + wrapIfLong(userSerialize(text)) + ". ")

    def addAction(self, name, details = ""):
        self.m_actionLog.append(TestAction(name, details))      
    
    def clickElementByName(self, name):
        self.addAction("click", "element name: " + userSerialize(name) + " ")
        self.getElementByName(name).click()
        self.checkPageErrors()

    def clickElementById(self, eleId):
        self.addAction("click", "element id: '" + eleId + "'")
        self.getElementById(eleId).click()
        self.checkPageErrors()
    
    def getElementText(self, xpath):
        try:
            return self.m_driver.find_element_by_xpath(xpath).text
        except NoSuchElementException:
            self.failTest("getElementText does not found xpath " + userSerialize(xpath) + ". ")
    
    def getElementTextById(self, eleId):
        self.checkEmptyParam(eleId, "getElementTextById")
        return self.getElementById(eleId).text

    # getPageTitle
    def getPageTitle(self):
        return self.m_driver.title
        
    def checkTextPresent(self, xpath, text):
        self.checkEmptyParam(xpath, "checkTextPresent")
        self.checkEmptyParam(text, "checkTextPresent")
        
        count = 0
        while count < 3:
            try:
                eleText = self.m_driver.find_element_by_xpath(xpath).text
                serOpt = []
                if xpath in ["/html/body", "//*"]: # too large
                    serOpt = ["cut_strings"]
                self.logAdd("checkTextPresent: current element by path " + userSerialize(xpath) + ", text: " + wrapIfLong(userSerialize(eleText, serOpt)) + ". ")
                if isList(text):
                    for phrase in text:
                        if phrase in eleText:
                            return True
                    return False
                else:
                    return text in eleText
            except InvalidSelectorException:
                self.failTest("Invalid XPath expression in checkTextPresent: " + userSerialize(xpath) + ". ")
            except NoSuchElementException:
                self.logAdd("checkTextPresent does not found XPath " + userSerialize(xpath) + ". ")
                return False
            except StaleElementReferenceException:
                self.logAdd("Cache problem in checkTextPresent. XPath: " + userSerialize(xpath) + ", text: " + wrapIfLong(userSerialize(text)) + ". Trying again. ")
                count += 1
                self.wait(1.0)
                continue
        self.failTest("Unsolvable cache problem in checkTextPresent. XPath: " + userSerialize(xpath) + ", text: " + wrapIfLong(userSerialize(text)) + ". ")
        
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
            self.failTest("Text " + userSerialize(text) + " not found on page " + userSerialize(self.curUrl()) + ", element " + userSerialize(xpath) + ". " + self.displayReason(reason))

    def assertTextNotPresent(self, xpath, text, forbidReason = ""):
        if self.checkTextPresent(xpath, text):
            errText = "Forbidden text " + userSerialize(text) + " found on page " + userSerialize(self.curUrl()) + ", element " + userSerialize(xpath) + ". " + self.displayReason(forbidReason)
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
            self.logAdd("Search for partial link text " + userSerialize(urlText) + ". ")
            searchMethod = self.m_driver.find_element_by_partial_link_text
        
        if isList(urlText):
            for urlName in urlText:
                try:
                    url = searchMethod(urlName)
                    return url.get_attribute("href");
                except NoSuchElementException:
                    self.logAdd("Tried to find url by name " + userSerialize(urlName) + ", not found. ")
                    pass
            else:
                # loop ended, found nothing
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = "Cannot find URL by link texts: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
                self.failTestWithItemNotFound(msg)
        else: # single link
            try:
                url = searchMethod(urlText)
                return url.get_attribute("href");
            except NoSuchElementException:
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = "Cannot find URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
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
                    self.failTest("No index in URL array with link text " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". ")
            else:
                raise RuntimeError("Something bad retrieved from find_elements_by_xpath: it's not a list of WebElement. ")
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
            self.failTestWithItemNotFound(msg)

            
    def logAdd(self, text, logLevel = "debug"):
        try:
            if not self.m_logStarted:
                self.logStart()
                
            logFile = open(self.m_logFile, 'a')
            fullLogText = text + "\n"
            logFile.write(fullLogText.encode("UTF-8"))
            print "LOG[" + logLevel + "]: " + fullLogText
            logFile.close()
        except IOError:
            raise RuntimeError("Cannot write message to log file " + userSerialize(self.m_logFile) + ". ")
        
    
    def getPageSource(self):
        return self.m_driver.page_source
        
    def checkPhpErrors(self):
        #print dir(self.m_driver);
        pageText = self.getPageSource()
        susp = ["Notice:", "Error:", "Warning:", "Fatal error:", "Parse error:"];
        for word in susp:
            if (word in pageText) and (" on line " in pageText):
                self.logAdd("PHP ERROR " + userSerialize(word) + " detected on page " + userSerialize(self.curUrl()) + ": ")
                self.logAdd("ERROR_PAGE_BEGIN =================")
                self.logAdd(pageText)
                self.logAdd("ERROR_PAGE_END ===================")
                return True, word
        return False, None
    
    def assertPhpErrors(self):
        checkResult, suspWord = self.checkPhpErrors()
        if checkResult:
            logMsg = "PHP error " + userSerialize(suspWord) + " detected on the page " + userSerialize(self.curUrl()) + ". "
            self.logAdd(logMsg, "warning")
            if not self.m_errorsAsWarnings:
                raise TestError(logMsg)
    

