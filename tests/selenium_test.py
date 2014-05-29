#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException
from selenium.webdriver.common.keys import Keys

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

    def serializeAction(self):
        return self.m_action + " " + self.m_details

# generic function to run any test.
def RunTest(test):
    try:
        test.init()
        test.run()
        test.logAdd(test.getName() + " TEST PASSED", "action")
        return 0
    except TestFatal as e:
#       test.printActionLog()
        test.handleTestFatal(e)
        return 2
    except TestError as e:
        test.handleTestFail(e)
        test.printActionLog()
        return 1
    except TestShutdown as e:
        test.handleShutdown(e)
        return 0
    except NoSuchWindowException as e:
        test.logAdd("Seems like browser window have been closed. ", "error")
        return 2
    except URLError as e:
        test.logAdd("URL error occured. Seems like browser connection error occured (window has been closed, etc). ", "error")
        return 2
    except HTTPException as e:
        test.logAdd("HTTP error occured. Seems like browser connection error occured (window has been closed, etc). ", "error")
        return 2
    except KeyboardInterrupt as e:
        test.logAdd("Keyboard interrupt received, stopping test suite. ")
        test.handleException(e)
        return 2
    except Exception as e:
        test.logAdd("Generic test exception: " + str(e))
        test.handleException(e)
        return 2

def colorStrL(string, color):
    """ Colors string using color """
    return "\x1b[1;{textColor}m{text}\x1b[0m".format(textColor = color, text = string)


def DecodeRunResult(result):
    if result == 0: return colorStrL("PASSED", 32)
    elif result == 1: return colorStrL("FAILED", 31)
    elif result == 2: return "FATAL ERROR"
    else: return "n/a"

def getValue(ele):
    return ele.get_attribute('value')

#main API wrapper for Webdriver.
class SeleniumTest(object):
    def __init__(self, baseUrl, params = []):
        self.m_testName = self.__class__.__name__
        self.m_baseUrl = baseUrl
        self.m_params = params

        self.initDefaults()

        if self.needDoc():
            print self.m_testName, "test info:"
            print self.getDoc().encode("UTF-8")
            raise TestShutdown("Display doc")

        if self.needLeaveBrowserOpen():
            self.setCloseOnExit(False)


#       self.m_driver.window_maximize()

    def initDefaults(self):
        self.m_checkErrors = True
        self.m_closeOnExit = True
        self.m_logStarted = False
        self.m_errorsAsWarnings = False
        self.m_doCheck404 = True
        self.m_textOnPage404 = "Page not found"

        self.m_logFile = self.m_testName + ".log" #"_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") +
        self.m_actionLog = []
        self.m_logCheckStopWords = []

    def init(self):
        self.m_baseUrl = self.fixBaseUrl(self.getBaseUrl())
        if self.useChrome():
            chromePath = "/usr/bin/chromedriver"
            if not os.path.exists(chromePath):
                self.fatalTest("Chrome Driver is not installed. Please obtain latest version from\nhttp://chromedriver.storage.googleapis.com/index.html ")
            self.m_driver = webdriver.Chrome("/usr/bin/chromedriver")
        else:
            profileDir = "./test_profile"
            shutil.rmtree(profileDir, ignore_errors = True)
            os.mkdir(profileDir)
            fp = webdriver.FirefoxProfile(profileDir)
            self.m_driver = webdriver.Firefox(fp)

        #self.maximizeWindow()

    def getName(self):
        return self.m_testName

    def getDoc(self):
        return self.__doc__

    def maximizeWindow(self):
        if hasattr(self, 'm_driver'):
            self.m_driver.maximize_window()

    def __del__(self):
        if hasattr(self, 'm_driver'):
            if self.m_closeOnExit:
                #self.logAdd("Closing webdriver. ")
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
        return exitCode # sys.exit(exitCode)

    def handleShutdown(self, exc):
        return self.shutdown(0)

    def handleException(self, exc):
        self.logAdd(self.getName() + " TEST GENERIC ERROR: " + userSerialize(exc.message), "error")
        self.logAdd("Traceback:\n" + traceback.format_exc())
        return self.shutdown(2)

    def handleTestFail(self, exc):
        #self.m_driver.execute_script("alert('Test failed! See console log for details. ');")
        self.logAdd(self.getName() + " TEST FAILED: " + userSerialize(exc.message), "error")
        return self.shutdown(1)

    def handleTestFatal(self, exc):
        #self.m_driver.execute_script("alert('Test fataled! See logs and check your test/environment. ');")
        self.logAdd(self.getName() + " TEST FATAL ERROR: " + userSerialize(exc.message), "fatal")
        self.logAdd("Traceback:\n" + traceback.format_exc())
        return self.shutdown(2)

    def getActionLog(self):
        # return copy of navigation log
        return self.m_actionLog[:]

    def printActionLog(self):
        self.logAdd("====== TEST " + self.getName() + " ACTION LOG: ======")
        for act in self.m_actionLog:
            self.logAdd("    " + act.serializeAction())
        self.logAdd("=" * 20)

    def logStart(self):
        try:
            logFile = open(self.m_logFile, "w")
            logText = "[" + self.m_testName + " log start on " + self.m_baseUrl + "]\n"
            logFile.write(logText.encode("UTF-8"))
            logFile.close()
            #indicate that log was already created
            self.m_logStarted = True
        except IOError:
            self.fatalTest("Cannot create log file " + userSerialize(self.m_logFile) + ". ")

    def setCloseOnExit(self, flag):
        self.m_closeOnExit = flag;

    # PHP errors auto-check toggle
    def setAutoPhpErrorChecking(self, checkErrors = True):
        self.m_checkErrors = checkErrors

    def set404Checking(self, value = True):
        if value:
            self.logAdd("Enabling 404 checking. ")
        else:
            self.logAdd("Disabling 404 checking. ")
        self.m_doCheck404 = value

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
            actionMsg += (" comment: " + userSerialize(comment) + " ")
        self.addAction("navigate", actionMsg)
        self.m_driver.get(fullUrl)

        self.checkPageErrors()
        self.check404()

    def checkPageErrors(self):
        if self.m_checkErrors:
            self.assertPhpErrors()

    def check404(self):
        if not self.m_doCheck404:
            return
        if self.checkSourceTextPresent(self.m_textOnPage404):
            self.failTest("Requested URL '" + userSerialize(self.curUrl()) + "' leads to non-existing page (404). ")

    def set404Text(self, text):
        self.m_textOnPage404 = text

    def gotoUrlByLinkText(self, linkName, reason = ""):
        """
        reason is custom comment helping to understand why this link is vital for test pass.
        """
        try:
            link = self.getUrlByLinkText(linkName, reason = reason)
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest("Cannot find URL with name " + userSerialize(linkName) + ". " + self.displayReason(reason))

    # TODO: Remove copypaste from gotoUrlByLinkText
    def gotoUrlByLinkTitle(self, linkName, reason = ""):
        """
        reason is custom comment helping to understand why this link is vital for test pass.
        """
        try:
            link = self.getUrlByLinkText(linkName, reason = reason, optionList = ["title"])
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest("Cannot find URL with name " + userSerialize(linkName) + ". " + self.displayReason(reason))

    def sendEnterById(self, eleId):
        self.checkEmptyParam(eleId, "sendEnterById")
        ele = self.getElementById(eleId)
        ele.send_keys(Keys.RETURN)
        
    def sendEnterByName(self, eleName):
        self.checkEmptyParam(eleName, "sendEnterByName")
        ele = self.getElementByName(eleName)
        ele.send_keys(Keys.RETURN)
        
    def gotoUrlByPartialLinkText(self, linkName, reason = ""):
        try:
            link = self.getUrlByLinkText(linkName, ["partial"], reason)
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

    def assertUrlNotPresent(self, linkName, reason = ""):
        try:
            self.getUrlByLinkText(linkName, reason = reason)
            exceptionMessage = "Forbidden URL is found on the page in assertUrlNotPresent: " + userSerialize(linkName) + ". " + self.displayReason(reason)
            self.failTest(exceptionMessage)
        except ItemNotFound:
            self.logAdd("URL " + userSerialize(linkName) + " is really not present (ItemNotFound exception raised). ")
            pass

    def assertUrlPresent(self, linkName, reason = ""):
        try:
            self.getUrlByLinkText(linkName, reason = reason)
        except ItemNotFound:
            exceptionMessage = "Required URL is not found on the page in assertUrlPresent: " + userSerialize(linkName) + ". " + self.displayReason(reason)
            self.failTest(exceptionMessage)

    def wait(self, seconds, comment = ""):
        self.logAdd("Waiting for " + userSerialize(seconds) + " seconds. Comment: " + userSerialize(comment))
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

    def checkCheckboxValueById(self, eleId, boolValue = True, reason = ""):
        self.checkEmptyParam(eleId, "checkCheckboxValueById")
        value = self.getElementById(eleId).get_attribute("checked")
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox '" + eleId + "': " + userSerialize(value)
            self.failTest(msg + self.displayReason(reason))

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

    def checkCheckboxValueByName(self, eleName, boolValue = True, reason = ""):
        self.checkEmptyParam(eleName, "checkCheckboxValueByName")
        value = self.getElementByName(eleName).get_attribute("checked")
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox " + userSerialize(eleName) + ": " + userSerialize(value)
            self.failTest(msg + self.displayReason(reason))

        if boolValue: # check if it is 'checked'
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:true, element name: " + userSerialize(eleName) + ". ")
                return True
            return False
        else: # check if it is unchecked
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:false, element name: " + userSerialize(eleName) + ". ")
                return False
            return True

    def assertCheckboxValueById(self, eleId, boolValue = True, reason = ""):
        if not self.checkCheckboxValueById(eleId, boolValue, reason):
            self.failTest("Checkbox with id '" + eleId + "' has improper value, expected " + userSerialize(boolValue) + ". " + self.displayReason(reason))

    def assertCheckboxValueByName(self, eleName, boolValue = True, reason = ""):
        if not self.checkCheckboxValueByName(eleName, boolValue, reason):
            self.failTest("Checkbox with name " + userSerialize(eleName) + " has improper value, expected " + userSerialize(boolValue) + ". " + self.displayReason(reason))

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
            ele = self.getElementById(eleId)
            self.logAdd("Sending text to element '" + eleId + "'")
            ele.send_keys(text)
            return getValue(self.getElementById(eleId))
        except InvalidElementStateException as e:
            self.fatalTest("Cannot set element value by id '" + eleId + "', possibly element is read-only.")

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
            self.fatalTest("Invalid index in setOptionValueByIdAndIndex for element " + eleId + ". Index should be positive (1 and above). ")
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
        testAction = TestAction(name, details)
        self.m_actionLog.append(TestAction(name, details))
        self.logAdd(testAction.serializeAction(), "action")

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

    # to filter log for regular messages like '404 not found'.
    def setLogStopWords(self, stopList):
        if isList(stopList):
            self.m_logCheckStopWords = stopList
        else:
            self.m_logCheckStopWords = [stopList]

    def isStopWord(self, text):
        return text in self.m_logCheckStopWords or text == self.m_textOnPage404

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

                if not self.isStopWord(text):
                    self.logAdd("checkTextPresent: element " + userSerialize(xpath) + " text: " + wrapIfLong(userSerialize(eleText, serOpt).replace("\n", " ")) + ". ")

                if isList(text):
                    for phrase in text:
                        if phrase in eleText:
                            self.logAdd("checkTextPresent: found phrase " + userSerialize(phrase) + " in element with xpath " + userSerialize(xpath) + ". ")
                            return True
                    self.logAdd("checkTextPresent: NOT found any of " + userSerialize(text) + " in element with xpath " + userSerialize(xpath) + ". ")
                    return False
                else:
                    bFound = text in eleText
                    particle = "" if bFound else "NOT "
                    if not self.isStopWord(text):
                        self.logAdd("checkTextPresent: " + particle + "found text " + userSerialize(text) + " in element with xpath " + userSerialize(xpath) + ". ")
                    return bFound

            except InvalidSelectorException:
                self.fatalTest("Invalid XPath expression in checkTextPresent: " + userSerialize(xpath) + ". ")
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

    def fatalTest(self, errorText):
        self.logAdd("TEST FATAL ERROR: " + userSerialize(errorText), "fatal")
        raise TestError(errorText)

    def failTest(self, errorText):
        self.logAdd("TEST FAILED: " + userSerialize(errorText), "error")
        raise TestError(errorText)

    def throwItemNotFound(self, errorText):
        self.logAdd("Item-Not-Found: " + userSerialize(errorText))
        raise ItemNotFound(errorText)

    def assertTextPresent(self, xpath, text, reason = ""):
        if not self.checkTextPresent(xpath, text):
            self.failTest("Text " + userSerialize(text) + " not found on page " + userSerialize(self.curUrl()) + ", element " + userSerialize(xpath) + ". " + self.displayReason(reason))

    def assertTextNotPresent(self, xpath, text, reason = ""):
        if self.checkTextPresent(xpath, text):
            errText = "Forbidden text " + userSerialize(text) + " found on page " + userSerialize(self.curUrl()) + ", element " + userSerialize(xpath) + ". " + self.displayReason(reason)
            self.failTest(errText)

    def assertBodyTextPresent(self, text, reason = ""):
        return self.assertTextPresent("/html/body", text, reason)

    def assertBodyTextNotPresent(self, text, reason = ""):
        return self.assertTextNotPresent("/html/body", text, reason)

    def assertSourceTextPresent(self, text, reason = ""):
        return self.assertTextPresent("//*", text, reason)

    def assertSourceTextNotPresent(self, text, reason = ""):
        return self.assertTextNotPresent("//*", text, reason)

    def checkEmptyParam(self, stringOrList, methodName):
        if isList(stringOrList):
            if len(stringOrList) == 0:
                self.fatalTest("Empty list passed to " + methodName)
            for text in stringOrList:
                if isVoid(text):
                    self.fatalTest("Empty string passed in the list to " + methodName)
        else:
            if isVoid(stringOrList):
                self.fatalTest("Empty param passed to " + methodName)

    def getUrlByLinkText(self, urlText, optionList=[], reason=""):

        self.checkEmptyParam(urlText, "getUrlByLinkText");
        searchMethod = self.m_driver.find_element_by_link_text
        if "partial" in optionList:
            self.logAdd("Search for partial link text " + userSerialize(urlText) + ". ")
            searchMethod = self.m_driver.find_element_by_partial_link_text
        elif "title" in optionList:
            self.logAdd("Search for link with title " + userSerialize(urlText) + ". ")
            searchMethod = self.m_driver.find_element_by_css_selector

        def getUrl(urlName, optionList=[]):
            if "title" in optionList:
                url = searchMethod('[title="' + urlName + '"]')
            else:
                url = searchMethod(urlName)
            return url.get_attribute("href");


        if isList(urlText):
            for urlName in urlText:
                try:
                    return getUrl(urlName, optionList=optionList)
                except NoSuchElementException:
                    self.logAdd("Tried to find url by name " + userSerialize(urlName) + ", not found. ")
            else:
                # loop ended, found nothing
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = "Cannot find URL by link texts: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". " + self.displayReason(reason)
                self.throwItemNotFound(msg)
        else: # single link
            try:
                return getUrl(urlText, optionList=optionList)
            except NoSuchElementException:
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = "Cannot find URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". " + self.displayReason(reason)
                self.throwItemNotFound(msg)

    def countIndexedUrlsByLinkText(self, urlText, sibling=""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling="text()"

            xpath = "//a[" + sibling + "='" + urlText + "']"
            urls = self.m_driver.find_elements_by_xpath(xpath)

            if not isList(urls):
                self.fatalTest("countIndexedUrlsByLinkText(): Something bad retrieved from find_elements_by_xpath: it's not a list of WebElement. ")

            listSize = len(urls)
            self.logAdd("Urls list size: " + userSerialize(listSize))
            return listSize
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
            self.throwItemNotFound(msg)


    def gotoIndexedUrlByLinkText(self, urlText, index, sibling = ""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling="text()"

            xpath = "//a[" + sibling + "='" + urlText + "']"
            urls = self.m_driver.find_elements_by_xpath(xpath)

            if not isList(urls):
                self.fatalTest("clickIndexedElementByText(): Something bad retrieved from find_elements_by_xpath: it's not a list of WebElement. ")

            self.logAdd("Urls list size: " + userSerialize(len(urls)))
            if index < len(urls):
                url = urls[index]
                href = url.get_attribute("href")
                self.logAdd("Found URL with index " + userSerialize(index) + ": " + href)
                if isVoid(href):
                    self.fatalTest("clickIndexedElementByText(): empty 'href' attribute of a-element with index " + userSerialize(index) )
                self.gotoSite(href)
            else:
                self.failTest("No index '" + userSerialize(index) + "' in URL array with link text " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". ")
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
            self.throwItemNotFound(msg)

    def logAdd(self, text, logLevel = "debug"):
        try:
            if not self.m_logStarted:
                self.logStart()

            fullLogText = self.getName() + "[" + logLevel + "]: " + text + "\n"
            print fullLogText.strip().encode("UTF-8")
            logFile = open(self.m_logFile, 'a')
            logFile.write(fullLogText.encode("UTF-8"))
            logFile.close()
        except IOError:
            self.fatalTest("Cannot write message to log file " + userSerialize(self.m_logFile) + ". ")


    def getPageSource(self):
        return self.m_driver.page_source

    def checkPhpErrors(self):
        pageText = self.getPageSource()
        susp = ["Notice:", "Error:", "Warning:", "Fatal error:", "Parse error:"]
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


