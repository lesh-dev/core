#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from urllib2 import URLError
from httplib import HTTPException

import traceback
import time
import os
import errno
import shutil

# from bawlib import isString
from bawlib import isVoid, isList, isNumber, isEqual, getSingleOption, userSerialize, wrapIfLong

MAX_RETRIES = 4
TIME_INC = 0.2

class TestError(RuntimeError):
    pass


class TestFatal(RuntimeError):
    pass


class ItemNotFound(TestError):
    pass


class PageNotFound(TestError):
    pass


class TestShutdown(RuntimeError):
    pass


class TestAction:
    def __init__(self, action, details):
        self.m_action = action
        self.m_details = details

    def serializeAction(self):
        return self.m_action + " " + self.m_details


def current_time():
    return time.time()


# generic function to run any test.
def RunTest(test):
    try:
        test.init()
        test.run()
        test.logAdd(test.getName() + " TEST PASSED", "action")
        return 0
    except TestFatal as exc:
        # test.printActionLog()
        return test.handleTestFatal(exc)
    except TestError as exc:
        return test.handleTestFail(exc)
        # test.printActionLog()
    except TestShutdown as exc:
        return test.handleShutdown(exc)
    except NoSuchWindowException as exc:
        test.logAdd("Seems like browser window have been closed. ", "error")
        return 3
    except URLError as exc:
        test.logAdd("URL error occured. Seems like browser connection error occured (window has been closed, etc). ", "error")
        return 3
    except HTTPException as exc:
        test.logAdd("HTTP error occured. Seems like browser connection error occured (window has been closed, etc). ", "error")
        return 3
    except KeyboardInterrupt as exc:
        test.logAdd("Keyboard interrupt received, stopping test suite. ")
        return 3
    except Exception as exc:
        test.logAdd(u"Generic test exception: " + userSerialize(exc.message))
        print traceback.format_exc()
        return test.handleException(exc)


def colorStrL(string, color):
    """ Colors string using color """
    return "\x1b[1;{textColor}m{text}\x1b[0m".format(textColor=color, text=string)


def DecodeRunResult(result):
    if result == 0:
        return colorStrL("PASSED", 32)
    elif result == 1:
        return colorStrL("FAILED", 31)
    elif result == 2:
        return colorStrL("FATAL ERROR", 33)
    elif result == 3:
        return colorStrL("STOPPED", 34)
    else:
        return "n/a"


def createLogDir(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def getValue(ele):
    return ele.get_attribute('value')


class SeleniumTest(object):
    """
        Main API wrapper for Webdriver
    """

    m_driver = None

    # defaults
    m_checkErrors = True
    m_closeOnExit = True
    m_logStarted = False
    m_errorsAsWarnings = False
    m_doCheck404 = True
    m_textOnPage404 = "Page not found"
    m_logDir = "logs"
    m_logFile = None
    m_actionLog = []
    m_logCheckStopWords = []
    m_old_firefox_driver = False

    def __init__(self, baseUrl, params=[]):
        self.m_testName = self.__module__ + "." + self.__class__.__name__
        self.m_baseUrl = baseUrl or ""
        self.m_params = params or []

        # time_suffix = "_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.m_logFile = self.m_logDir + "/" + self.m_testName + ".log"

        if self.needDoc():
            print self.m_testName, "test info:"
            print self.getDoc().encode("UTF-8")
            raise TestShutdown("Display doc")

        if self.needLeaveBrowserOpen():
            self.setCloseOnExit(False)

        # self.m_driver.window_maximize()

    def init(self):
        self.m_baseUrl = self.fixBaseUrl(self.getBaseUrl())
        if self.useChrome():
            chrome_path = "/usr/bin/chromedriver"
            if not os.path.exists(chrome_path):
                self.fatalTest(
                    "Chrome Driver is not installed. Please obtain latest version from\n"
                    "http://chromedriver.storage.googleapis.com/index.html "
                )
            self.m_driver = webdriver.Chrome(
                executable_path="/usr/bin/chromedriver",
            )
        else:
            profile_dir = "./test_profile"
            shutil.rmtree(profile_dir, ignore_errors=True)
            os.mkdir(profile_dir)
            if self.m_old_firefox_driver:
                fp = webdriver.FirefoxProfile(profile_dir)
                self.m_driver = webdriver.Firefox(fp)
            else:
                firefox_profile = webdriver.FirefoxProfile(profile_dir)
                firefox_profile.set_preference("security.ssl.enable_ocsp_stapling", False)
                firefox_profile.set_preference("security.ssl.enable_ocsp_must_staple", False)
                firefox_profile.set_preference("security.OCSP.enabled", 0)
                firefox_profile.update_preferences()

                # see this fine manual about how it's difficult to live under Fx47+
                # https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver
                caps = DesiredCapabilities.FIREFOX
                caps["marionette"] = True
                caps["binary"] = "/usr/bin/firefox"
                self.m_driver = webdriver.Firefox(
                    firefox_profile=firefox_profile,
                    capabilities=caps,
                    executable_path="/usr/bin/geckodriver",
                )

        # self.maximizeWindow()

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
                pass
                # self.logAdd("Closing webdriver. ")
                # self.m_driver.quit()

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
        opt, _ = getSingleOption(["-p", "--preserve"], self.m_params)
        return opt

    def shutdown(self, exitCode=0):
        return exitCode

    def handleShutdown(self, exc):
        return self.shutdown(0)

    def handleException(self, exc):
        self.logAdd(self.getName() + " TEST GENERIC ERROR: " + userSerialize(exc.message), "error")
        return self.shutdown(2)

    def handleTestFail(self, exc):
        self.logAdd(self.getName() + " TEST FAILED: " + userSerialize(exc.message), "error")
        return self.shutdown(1)

    def handleTestFatal(self, exc):
        self.logAdd(self.getName() + " TEST FATAL ERROR: " + userSerialize(exc.message), "fatal")
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
            createLogDir(self.m_logDir)
            logFile = open(self.m_logFile, "w")
            logText = "[" + self.m_testName + " log start on " + self.m_baseUrl + "]\n"
            logFile.write(logText.encode("UTF-8"))
            logFile.close()
            # indicate that log was already created
            self.m_logStarted = True
            self.m_logTime = current_time()
        except IOError:
            self.fatalTest("Cannot create log file " + userSerialize(self.m_logFile) + ". ")

    def setCloseOnExit(self, flag):
        self.m_closeOnExit = flag

    # PHP errors auto-check toggle
    def setAutoPhpErrorChecking(self, checkErrors=True):
        self.m_checkErrors = checkErrors

    def set404Checking(self, value=True):
        if value:
            self.logAdd("Enabling 404 checking. ")
        else:
            self.logAdd("Disabling 404 checking. ")
        self.m_doCheck404 = value

    def setPhpErrorsAsWarnings(self, errorsAsWarnings=True):
        self.m_errorsAsWarnings = errorsAsWarnings

    def fixBaseUrl(self, url):
        if isVoid(url):
            raise TestError("Test base URL is empty. Nowhere to run. ")
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        return url

    # get current URL of tested site
    def curUrl(self):
        return self.m_driver.current_url

    def gotoRoot(self):
        return self.gotoPage("/")

    # alias of gotoPage, for similarity with gotoUrlByLinkText
    def gotoUrl(self, url, comment=""):
        return self.gotoPage(url, comment)

    # @comment usually means link name (or id), which we used to navigate to this URL.
    def gotoPage(self, url, comment=""):
        normUrl = url
        if not normUrl.startswith("/"):
            normUrl = "/" + normUrl
        fullUrl = self.m_baseUrl + normUrl
        return self.gotoSite(fullUrl, comment)

    def lastActionType(self):
        if self.m_actionLog:
            return self.m_actionLog[-1].m_action
        return "none"

    # @comment usually means link name (or id), which we used to navigate to this URL.
    def gotoSite(self, fullUrl, comment=""):
        actionMsg = "Link: " + userSerialize(fullUrl)
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
            raise PageNotFound(
                "Requested URL '{}' leads to non-existing page (404). ".format(userSerialize(self.curUrl()))
            )

    def set404Text(self, text):
        self.m_textOnPage404 = text

    def isBaseUrl(self, link):
        pfxList = ["http://", "https://"]
        pureBaseUrl = self.m_baseUrl
        pureLink = link
        for pfx in pfxList:
            pureBaseUrl = pureBaseUrl.replace(pfx, "", 1)
            pureLink = pureLink.replace(pfx, "", 1)

        if not pureLink.startswith(pureBaseUrl):
            return False
        return True

    def checkBaseUrl(self, link):
        if not self.isBaseUrl(link):
            self.failTest(
                "Link with name " + userSerialize(link) + " leads to another site: " + userSerialize(link) + ". "
            )

    def gotoUrlByLinkText(self, linkName, reason=""):
        """
        reason is custom comment helping to understand why this link is vital for test pass.
        """
        try:
            link = self.getUrlByLinkText(linkName, reason=reason)
            self.checkBaseUrl(link)
            self.gotoSite(link, linkName)
        except NoSuchElementException:
            self.failTest("Cannot find URL with name " + userSerialize(linkName) + ". " + self.displayReason(reason))

    # TODO: Remove copypaste from gotoUrlByLinkText
    def gotoUrlByLinkTitle(self, linkName, reason=""):
        """
        reason is custom comment helping to understand why this link is vital for test pass.
        """
        try:
            link = self.getUrlByLinkText(linkName, reason=reason, option_list=["title"])
            self.checkBaseUrl(link)
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

    def gotoUrlByPartialLinkText(self, linkName, reason=""):
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

    def assertUrlNotPresent(self, linkName, reason=""):
        try:
            self.getUrlByLinkText(linkName, reason=reason, option_list=["silent"])
            exMsg = "Forbidden URL is found on the page in assertUrlNotPresent: " + userSerialize(linkName) + ". " + self.displayReason(reason)
            self.failTest(exMsg)
        except ItemNotFound:
            self.logAdd(u"URL " + userSerialize(linkName) + " is really not present (ItemNotFound exception raised). ")

    def assertPageNotPresent(self, pageUrl, reason=""):
        try:
            self.gotoPage(pageUrl)
            exMsg = "Forbidden page is found while going to URL in assertPageNotExists: " + userSerialize(pageUrl) + ". " + self.displayReason(reason)
            self.failTest(exMsg)
        except PageNotFound:
            self.logAdd(u"Page " + userSerialize(pageUrl) + " is really not present (PageNotFound exception raised). ")

    def assertUrlPresent(self, linkName, reason=""):
        try:
            self.getUrlByLinkText(linkName, reason=reason)
        except ItemNotFound:
            exceptionMessage = "Required URL is not found on the page in assertUrlPresent: " + userSerialize(linkName) + ". " + self.displayReason(reason)
            self.failTest(exceptionMessage)

    def wait(self, seconds, comment=""):
        self.addAction("wait", "Waiting for " + userSerialize(seconds) + " seconds. Comment: " + userSerialize(comment))
        if seconds <= 3.0:
            time.sleep(seconds)
            return
        quant = 3
        seconds = int(seconds)
        periods = seconds // quant
        for i in xrange(periods):
            time.sleep(quant)
            self.logAdd("Passed {0} seconds of {1}".format((i + 1) * quant, seconds))
        time.sleep(seconds % quant)

    def drv(self):
        return self.m_driver

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

    def getElementByClass(self, css_class):
        try:
            return self.m_driver.find_element_by_css_selector(css_class)
        except NoSuchElementException:
            self.failTest("Cannot get element by class '" + css_class + "'. ")

    def executeJS(self, script):
        return self.m_driver.execute_script(script)

    def checkboxIsValid(self, value):
        return value == "checked" or value == "true"

    def checkCheckboxValueById(self, eleId, boolValue=True, reason=""):
        self.checkEmptyParam(eleId, "checkCheckboxValueById")
        value = self.getElementById(eleId).get_attribute("checked")
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox '" + eleId + "': " + userSerialize(value)
            self.failTest(msg + self.displayReason(reason))

        if boolValue:  # check if it is 'checked'
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:true, element id: '" + eleId + "'. ")
                return True
            return False
        else:  # check if it is unchecked
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:false, element id: '" + eleId + "'. ")
                return False
            return True

    def checkCheckboxValueByName(self, eleName, boolValue=True, reason=""):
        self.checkEmptyParam(eleName, "checkCheckboxValueByName")
        value = self.getElementByName(eleName).get_attribute("checked")
        if value and not self.checkboxIsValid(value):
            msg = "Strange value for checkbox " + userSerialize(eleName) + ": " + userSerialize(value)
            self.failTest(msg + self.displayReason(reason))

        if boolValue:  # check if it is 'checked'
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:true, element name: " + userSerialize(eleName) + ". ")
                return True
            return False
        else:  # check if it is unchecked
            if value and self.checkboxIsValid(value):
                self.logAdd("check-box:false, element name: " + userSerialize(eleName) + ". ")
                return False
            return True

    def assertCheckboxValueById(self, eleId, boolValue=True, reason=""):
        if not self.checkCheckboxValueById(eleId, boolValue, reason):
            self.failTest("Checkbox with id '" + eleId + "' has improper value, expected " + userSerialize(boolValue) + ". " + self.displayReason(reason))

    def assertCheckboxValueByName(self, eleName, boolValue=True, reason=""):
        if not self.checkCheckboxValueByName(eleName, boolValue, reason):
            self.failTest(
                "Checkbox with name " + userSerialize(eleName) +
                " has improper value, expected " + userSerialize(boolValue) + ". " + self.displayReason(reason)
            )

    def fillElementByName(self, name, text, clear=True):
        self.checkEmptyParam(name, "fillElementByName")
        if clear:
            self.addAction("clear", "element name: " + userSerialize(name) + " ")
            self.getElementByName(name).clear()
        self.addAction("fill", "element name: " + userSerialize(name) + ", text: " + wrapIfLong(userSerialize(text)) + " ")
        self.getElementByName(name).send_keys(text)
        return getValue(self.getElementByName(name))

    def fillElementById(self, eleId, text, clear=True):
        try:
            self.checkEmptyParam(eleId, "fillElementById")
            ele = self.getElementById(eleId)
            if clear:
                self.addAction("clear", "element id: '" + eleId + "'")
                ele.clear()

            self.addAction("fill", "element id: '" + eleId + "', text: " + wrapIfLong(userSerialize(text)) + " ")
            self.logAdd("Sending text to element '" + eleId + "'")
            ele = self.getElementById(eleId)  # Selenium element cache miss can occur
            ele.send_keys(text)
            return getValue(ele)
        except InvalidElementStateException:
            self.fatalTest("Cannot set element value by id '" + eleId + "', possibly element is read-only.")

    def escapeJSString(self, text):
        return text.replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")

    def fillAceEditorElement(self, text, clear=True):
        eleClass = 'textarea.ace_text-input'  # a bit of hardcode, we have only one ACE editor on screen at a time
        ele = self.getElementByClass(eleClass)
        if clear:
            self.addAction("clear", "element class: '" + eleClass + "'")
            ele.clear()

        self.addAction("fill", "element: ACE, text: " + wrapIfLong(userSerialize(text)) + " ")
        self.logAdd("Sending text to ACE element")
        # send_keys works bad in case of ACE, so we use its JS methods
        # ele.send_keys(text)
        self.executeJS("return $('#edit-text').data('editor-ref').setValue('" + self.escapeJSString(text) + "');")
        return self.executeJS("return $('#edit-text').data('editor-ref').getValue();")

    def checkAceEditorElementText(self, text):
        eleClass = 'textarea.ace_text-input'  # a bit of hardcode, we have only one ACE editor on screen at a time
        # defeat cache
        self.getElementByClass(eleClass)
        self.addAction("check-text", "element: ACE, expected: " + wrapIfLong(userSerialize(text)) + ". ")
        currentText = self.executeJS("return $('#edit-text').data('editor-ref').getValue();")
        if isEqual(text, currentText):
            self.addAction("check-text:ok", "element: ACE")
            return True
        self.addAction(
            "check-text:fail",
            "element: ACE, actual: " + wrapIfLong(userSerialize(currentText)) + ", expected: " + wrapIfLong(userSerialize(text)) + " "
        )
        return False

    def assertAceEditorElementText(self, text, reason=""):
        if not self.checkAceEditorElementText(text):
            self.failTest("ACE element text does not match expected: " + wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason))

    # by id
    def setOptionValueByIdAndValue(self, eleId, optValue):
        if isNumber(optValue):
            optValue = str(optValue)
        self.addAction("set-option-by-value", "element id: '" + eleId + "', value: " + userSerialize(optValue))

        selector = None
        try:
            selector = self.getElementById(eleId)
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by id '" + eleId + "'. ")

        xpath = "option[@value='" + optValue + "']"
        try:
            option = selector.find_element_by_xpath(xpath)
            option.click()
        except NoSuchElementException:
            self.failTest("Cannot find selector option by xpath " + xpath)

    def setOptionValueByIdAndIndex(self, eleId, index):
        """
        element index is started with 1, not 0.
        """
        optionValue, text = self.getOptionValueByIdAndIndex(eleId, index)
        self.addAction("set-option-by-index", "element id: '" + eleId + "', index: " + userSerialize(index))
        self.setOptionValueByIdAndValue(eleId, optionValue)

    # by name
    def setOptionValueByNameAndValue(self, eleName, optValue):
        try:
            if isNumber(optValue):
                optValue = str(optValue)
            self.addAction("set-option-by-value", "element name: '" + eleName + "', value: " + userSerialize(optValue))

            self.getElementByName(eleName).find_element_by_xpath("option[@value='" + optValue + "']").click()
            self.checkPageErrors()
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by name '" + eleName + "'. ")

    # returns option value (index) and text
    def getOptionValueByIdAndIndex(self, eleId, index):
        """
        element index is started with 1, not 0.
        """
        if index < 1:
            self.fatalTest("Invalid index in getOptionValueByIdAndIndex for element " + eleId + ". Index should be positive (1 and above). ")
        self.addAction("get-option-by-index", "element id: '" + eleId + "', index: " + userSerialize(index))
        selEle = self.getElementById(eleId)
        eleList = selEle.find_elements_by_xpath("option")
        actLen = len(eleList)
        if index >= actLen:
            self.failTest(
                "Index in getOptionValueByIdAndIndex is too large for element {0}. "
                "Option list size is {1}, requested index: {2}".format(eleId, actLen, index)
            )
        oneOption = selEle.find_element_by_xpath("option[" + userSerialize(index) + "]")
        return getValue(oneOption), oneOption.text

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
        self.logAdd(
            "check-value:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) +
            ", actual: " + wrapIfLong(userSerialize(eleValue)) + ". "
        )
        return False

    def checkElementTextById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementTextById")
        self.addAction("check-text", "element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
        eleText = self.getElementTextById(eleId)
        self.logAdd("checkElementTextById: current element '" + eleId + "', text is: " + wrapIfLong(userSerialize(eleText)) + ". ")
        if isEqual(eleText, text):
            self.logAdd("check-text:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.logAdd(
            "check-text:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) +
            ", actual: " + wrapIfLong(userSerialize(eleText)) + ". "
        )
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
        self.logAdd(
            "check-subtext:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) +
            ", actual: " + wrapIfLong(userSerialize(eleText)) + ". "
        )
        return False

    def assertElementSubTextById(self, eleId, text, reason=""):
        if not self.checkElementSubTextById(eleId, text):
            self.failTest(
                "Element with id '" + eleId + "' text does not contain expected: " + wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason)
            )

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
        self.logAdd(
            "check-value:fail, element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) +
            ", actual: " + wrapIfLong(userSerialize(eleValue)) + ". "
        )
        return False

    def assertElementTextById(self, eleId, text, reason=""):
        if not self.checkElementTextById(eleId, text):
            self.failTest(
                "Element with id '" + eleId + "' text does not match expected: " +
                wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason)
            )

    def assertElementValueById(self, eleId, text, reason=""):
        if not self.checkElementValueById(eleId, text):
            self.failTest(
                "Element with id '" + eleId + "' value does not match expected: " +
                wrapIfLong(userSerialize(text)) + ". " + self.displayReason(reason)
            )

    def assertElementValueByName(self, name, text):
        if not self.checkElementValueByName(name, text):
            self.failTest("Element with name '" + userSerialize(name) + " value does not match expected: " + wrapIfLong(userSerialize(text)) + ". ")

    def addAction(self, name, details=""):
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

    def checkTextPresent(self, xpath, text, option_list=None):
        option_list = option_list or []

        self.checkEmptyParam(xpath, "checkTextPresent")
        self.checkEmptyParam(text, "checkTextPresent")

        count = 0
        wait_time = 0.0
        while count < MAX_RETRIES:
            self.wait(wait_time, u"Checking for text '" + userSerialize(text) + u"'")
            count += 1
            wait_time += TIME_INC
            try:
                is_found = self.check_text_present_once(xpath, text, option_list)
                if is_found:
                    return True
                logging.info("checkTextPresent(): expected text not found, retrying.")
                continue
            except InvalidSelectorException:
                self.fatalTest("Invalid XPath expression in checkTextPresent: " + userSerialize(xpath) + ". ")
            except NoSuchElementException:
                self.logAdd("checkTextPresent does not found XPath " + userSerialize(xpath) + ". ")
                return False
            except StaleElementReferenceException:
                self.logAdd(
                    "Cache problem in checkTextPresent. XPath: " + userSerialize(xpath) +
                    ", text: " + wrapIfLong(userSerialize(text)) + ". Trying again. "
                )
                continue
        # not found
        return False

    def check_text_present_once(self, xpath, text, option_list):
        ele_text = self.m_driver.find_element_by_xpath(xpath).text
        ser_opt = []
        if xpath in ["/html/body", "//*"]:  # too large
            ser_opt = ["cut_strings"]

        if not self.isStopWord(text) and "silent" not in option_list:
            self.logAdd(
                "checkTextPresent: element " + userSerialize(xpath) + " text: " +
                wrapIfLong(userSerialize(ele_text, ser_opt).replace("\n", " ")) + ". "
            )

        if isList(text):
            for phrase in text:
                if phrase in ele_text:
                    self.logAdd("checkTextPresent: found phrase " + userSerialize(
                        phrase) + " in element with xpath " + userSerialize(xpath) + ". ")
                    return True
            if "silent" not in option_list:
                self.logAdd("checkTextPresent: NOT found any of " + userSerialize(
                    text) + " in element with xpath " + userSerialize(xpath) + ". ")
            return False
        else:
            is_found = text in ele_text
            particle = "" if is_found else "NOT "
            if not self.isStopWord(text):
                self.logAdd(
                    "checkTextPresent: " + particle + "found text " + userSerialize(text) +
                    " in element with xpath " + userSerialize(xpath) + ". "
                )
            return is_found

    def checkSourceTextPresent(self, text, option_list=None):
        option_list = option_list or []
        self.checkEmptyParam(text, "checkSourceTextPresent")

        count = 0
        wait_time = 0.0
        while count < MAX_RETRIES:
            self.wait(wait_time, u"Checking for source text '" + userSerialize(text) + u"'")
            count += 1
            wait_time += TIME_INC
            is_found = self.check_source_text_present_once(text, option_list)
            if is_found:
                return True
            logging.info("checkSourceTextPresent(): expected text not found, retrying.")
        # not found
        return False

    def check_source_text_present_once(self, text, option_list=None):

        option_list = option_list or []
        ele_text = self.getPageSource()
        ser_opt = ["cut_strings"]

        if not self.isStopWord(text) and "silent" not in option_list:
            self.logAdd(
                "checkSourceTextPresent: text: " +
                wrapIfLong(userSerialize(ele_text, ser_opt).replace("\n", " ")) + ". "
            )

        if isList(text):
            for phrase in text:
                if phrase in ele_text:
                    self.logAdd("checkSourceTextPresent: found phrase " + userSerialize(phrase) + " on page. ")
                    return True
            if "silent" not in option_list:
                self.logAdd("checkSourceTextPresent: NOT found any of " + userSerialize(text) + " on page. ")
            return False
        else:
            bFound = text in ele_text
            particle = "" if bFound else "NOT "
            if not self.isStopWord(text):
                self.logAdd("checkSourceTextPresent: " + particle + "found text " + userSerialize(text) + " on page. ")
            return bFound

    def checkBodyTextPresent(self, text, option_list=None):
        return self.checkTextPresent("/html/body", text, option_list=option_list)

    def fatalTest(self, errorText):
        self.logAdd("TEST FATAL ERROR: " + userSerialize(errorText), "fatal")
        raise TestFatal(errorText)

    def assertEqual(self, got_value, expected_value, error_text):
        if got_value != expected_value:
            error_text += "Expected '" + expected_value + "', got '" + got_value + "'. "
            self.logAdd("TEST FAILED: " + userSerialize(error_text), "error")
            raise TestError(error_text)

    def failTest(self, errorText):
        self.logAdd("TEST FAILED: " + userSerialize(errorText), "error")
        raise TestError(errorText)

    def throwItemNotFound(self, errorText, option_list=None):
        option_list = option_list or []
        if "silent" not in option_list:
            self.logAdd("Item-Not-Found: " + userSerialize(errorText))
        raise ItemNotFound(errorText)

    def assertTextPresent(self, xpath, text, reason=""):
        if not self.checkTextPresent(xpath, text):
            self.failTest(
                "Text " + userSerialize(text) + " not found on page " + userSerialize(self.curUrl()) +
                ", element " + userSerialize(xpath) + ". " + self.displayReason(reason)
            )

    def assertTextNotPresent(self, xpath, text, reason=""):
        if self.checkTextPresent(xpath, text):
            errText = (
                "Forbidden text " + userSerialize(text) + " found on page " + userSerialize(self.curUrl()) +
                ", element " + userSerialize(xpath) + ". " + self.displayReason(reason)
            )
            self.failTest(errText)

    def assertBodyTextPresent(self, text, reason=""):
        return self.assertTextPresent("/html/body", text, reason)

    def assertBodyTextNotPresent(self, text, reason=""):
        return self.assertTextNotPresent("/html/body", text, reason)

    def assertSourceTextPresent(self, text, reason=""):
        if not self.checkSourceTextPresent(text):
            self.failTest(
                "Text " + userSerialize(text) + " not found on page " + userSerialize(self.curUrl()) +
                ". " + self.displayReason(reason)
            )

    def assertSourceTextNotPresent(self, text, reason=""):
        if self.checkSourceTextPresent(text):
            errText = "Forbidden text " + userSerialize(text) + " found on page " + userSerialize(self.curUrl()) + ". " + self.displayReason(reason)
            self.failTest(errText)

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

    def getUrlByLinkText(self, urlText, option_list=None, reason=""):

        option_list = option_list or []

        self.checkEmptyParam(urlText, "getUrlByLinkText")
        searchMethod = self.m_driver.find_element_by_link_text
        if "partial" in option_list:
            self.logAdd("Search for partial link text " + userSerialize(urlText) + ". ")
            searchMethod = self.m_driver.find_element_by_partial_link_text
        elif "title" in option_list:
            self.logAdd("Search for link with title " + userSerialize(urlText) + ". ")
            searchMethod = self.m_driver.find_element_by_css_selector

        def getUrl(url_name, option_list=None):
            if not option_list:
                option_list = []
            if "title" in option_list:
                url = searchMethod('[title="' + url_name + '"]')
            else:
                url = searchMethod(url_name)
            return url.get_attribute("href")

        if isList(urlText):
            for urlName in urlText:
                try:
                    return getUrl(urlName, option_list=option_list)
                except NoSuchElementException:
                    if "silent" not in option_list:
                        self.logAdd("Tried to find url by name " + userSerialize(urlName) + ", not found. ")
            else:
                # loop ended, found nothing
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = (
                    "Cannot find URL by link texts: " + userSerialize(urlText) +
                    " on page " + userSerialize(self.curUrl()) + ". " + self.displayReason(reason)
                )
                self.throwItemNotFound(msg, option_list=option_list)
        else:  # single link
            try:
                return getUrl(urlText, option_list=option_list)
            except NoSuchElementException:
                # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
                msg = "Cannot find URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". " + self.displayReason(reason)
                self.throwItemNotFound(msg, option_list=option_list)

    def countIndexedUrlsByLinkText(self, urlText, sibling=""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling = "text()"

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

    def gotoIndexedUrlByLinkText(self, urlText, index, sibling=""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling = "text()"

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
                    self.fatalTest(
                        "clickIndexedElementByText(): empty 'href' attribute of a-element with index " + userSerialize(index)
                    )
                self.gotoSite(href)
            else:
                self.failTest(
                    "No index '" + userSerialize(index) + "' in URL array with link text " +
                    userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
                )
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
            self.throwItemNotFound(msg)

    def logAdd(self, text, logLevel="debug"):
        try:
            if not self.m_logStarted:
                self.logStart()

            newTime = current_time()
            duration = newTime - self.m_logTime
            self.m_logTime = newTime
            fullLogText = u"[{level:8}][{dur:06.2f}]: ".format(level=logLevel, dur=duration) + text.strip()
            print fullLogText.encode("UTF-8")
            logFile = open(self.m_logFile, 'a')
            logFile.write((fullLogText + "\n").encode("UTF-8"))
            logFile.close()
        except IOError:
            self.fatalTest("Cannot write message to log file " + userSerialize(self.m_logFile) + ". ")

    # alias for getPageSource
    def getPageContent(self):
        return self.getPageSource()

    def getPageSource(self):
        page_source = self.m_driver.page_source
        with open("current-page.html", "w") as page_fd:
            page_fd.write(page_source.encode("utf-8"))
        return page_source


    def checkPhpErrors(self):
        """
            returns True and suspicious word if error found, False/None otherwise
        """
        pageText = self.getPageSource()
        susp = [
            "Notice:",
            "Error:",
            "Warning:",
            "Fatal error:",
            "Parse error:",
            "Cannot find template:",
            "/var/www/",
            "/srv/www/",
        ]
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
            logMsg = "PHP ERROR " + userSerialize(suspWord) + " detected on the page " + userSerialize(self.curUrl()) + ". "
            self.logAdd(logMsg, "warning")
            if not self.m_errorsAsWarnings:
                raise TestError(logMsg)
