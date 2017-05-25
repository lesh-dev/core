#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import threading

from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import InvalidElementStateException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver.common.action_chains import ActionChains

from urllib2 import URLError
from httplib import HTTPException

import traceback
import time
import os
import errno
import shutil

from bawlib import isVoid, isList, isNumber, isEqual, getSingleOption, userSerialize, wrapIfLong
from bawlib import configure_logger

configure_logger()

MAX_RETRIES = 6
MAX_RETRIES_NEGATIVE = 2
TIME_INC = 0.05


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


class BrowserHolderException(Exception):
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
        logging.info("NoSuchWindowException: %s, %s", exc, traceback.format_exc())
        return 3
    except URLError as exc:
        test.logAdd("URL error occured. Seems like browser connection error occured (window has been closed, etc). ",
                    "error")
        logging.info("URLerror: %s, %s", exc, traceback.format_exc())
        return 3
    except HTTPException as exc:
        test.logAdd("HTTP error occured. Seems like browser connection error occured (window has been closed, etc). ",
                    "error")
        logging.info("HTTPException: %s, %s", exc, traceback.format_exc())
        return 3
    except KeyboardInterrupt as exc:
        test.logAdd("Keyboard interrupt received, stopping test suite. ")
        logging.info("KeyboardInterrupt: %s, %s", exc, traceback.format_exc())
        return 3
    except Exception as exc:
        test.logAdd(
            u"Generic test exception: " + userSerialize(str(exc)).decode('utf-8') +
            u", traceback:\n" + traceback.format_exc().decode('utf-8')
        )
        print traceback.format_exc()
        return test.handleException(exc)


def color_str_l(string, color):
    """ Colors string using color """
    return "\x1b[1;{textColor}m{text}\x1b[0m".format(textColor=color, text=string)


def decode_run_result(result):
    if result == 0:
        return color_str_l("PASSED", 32)
    elif result == 1:
        return color_str_l("FAILED", 31)
    elif result == 2:
        return color_str_l("FATAL ERROR", 33)
    elif result == 3:
        return color_str_l("STOPPED", 34)
    else:
        return "n/a"


def create_log_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def get_value(ele):
    return ele.get_attribute('value')


class BrowserHolder(object):

    def __init__(self, profile_path=None):
        self.driver = None
        self.already_initialized = False
        self.profile_path = profile_path

    # lazy init
    def init(self, use_chrome=False):
        with threading.Lock():
            # currently we have just one thread, but...
            if self.already_initialized:
                logging.info("Browser already initialized, doing nothing")
                return

            logging.info("Initializing browser")
            if use_chrome:
                self.driver = BrowserHolder.chrome_driver_instance()
            else:
                self.driver = BrowserHolder.firefox_driver_instance(self.profile_path)
            self.already_initialized = True

    @staticmethod
    def chrome_driver_instance():
        logging.info("Using Chrome")
        chrome_path_list = [
            "/usr/bin/chromedriver",
            "/usr/lib/chromium-browser/chromedriver",
        ]
        for chrome_path in chrome_path_list:
            if os.path.exists(chrome_path):
                logging.info("Using chrome driver from %s", chrome_path)
                return webdriver.Chrome(
                    executable_path=chrome_path,
                )

        raise BrowserHolderException("Chrome Driver is not installed. Install it from {}".format(distro_url))
        
        

    @staticmethod
    def firefox_driver_instance(profile_path):
        logging.info("Using Firefox")

        if profile_path is None:
            profile_path = "./test_profile"
            logging.info("Re-creating profile directory %s", profile_path)
            shutil.rmtree(profile_path, ignore_errors=True)
            os.mkdir(profile_path)
        else:
            logging.info("Using existing profile directory %s", profile_path)

        logging.info("Creating webdriver instance")
        firefox_profile = webdriver.FirefoxProfile(profile_path)
        firefox_profile.set_preference("security.ssl.enable_ocsp_stapling", False)
        firefox_profile.set_preference("security.ssl.enable_ocsp_must_staple", False)
        firefox_profile.set_preference("security.OCSP.enabled", 0)
        firefox_profile.update_preferences()

        # see this fine manual about how it's difficult to live under Fx47+
        # https://developer.mozilla.org/en-US/docs/Mozilla/QA/Marionette/WebDriver
        caps = DesiredCapabilities.FIREFOX
        caps["marionette"] = True
        caps["binary"] = "/usr/bin/firefox"
        return webdriver.Firefox(
            executable_path="/usr/bin/geckodriver",
            firefox_profile=firefox_profile,
            capabilities=caps,
        )


class SeleniumTest(object):
    """
        Main API wrapper for Webdriver
    """

    # defaults

    def __init__(self, base_url, browser_holder, params=None):
        """
        :type base_url: str
        :type browser_holder: BrowserHolder
        :type params: list | None
        """
        assert isinstance(base_url, str), "base_url should has type 'str'"
        assert isinstance(browser_holder, BrowserHolder), "browser_holder should have type 'BrowserHolder'"
        assert params is None or isinstance(params, list), "params should be 'list' or None"

        self.check_errors = True
        self.log_started = False
        self.errors_as_warnings = False
        self.do_check_404 = True
        self.text_on_page_404 = "Page not found"
        self.log_dir = "logs"
        self.log_file = None
        self.log_time = None
        self.action_log = []
        self.log_check_stop_words = []

        self.test_name = self.__module__ + "." + self.__class__.__name__
        self.base_url = base_url or ""
        self.params = params or []
        self.browser_holder = browser_holder

        # time_suffix = "_" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log_file = os.path.join(self.log_dir, "{}.log".format(self.test_name))

        if self.needDoc():
            print self.test_name, "test info:"
            print self.getDoc().encode("UTF-8")
            raise TestShutdown("Display doc")

    @property
    def m_driver(self):
        if not self.browser_holder:
            raise Exception("Browser holder is not initialized.")
        return self.browser_holder.driver

    def init(self):
        self.base_url = self.fixBaseUrl(self.getBaseUrl())
        self.browser_holder.init(use_chrome=self.use_chrome())

    def getName(self):
        return self.test_name

    def getDoc(self):
        return self.__doc__

    def getBaseUrl(self):
        if isVoid(self.base_url):
            self.failTest("Base URL for test '" + self.getName() + "' is not set. ")
        return self.base_url

    def use_chrome(self):
        chrome_flag, _ = getSingleOption(["-c", "--chrome"], self.params)
        return chrome_flag

    def needDoc(self):
        opt, _ = getSingleOption(["-d", "--doc"], self.params)
        return opt

    def shutdown(self, exit_code=0):
        return exit_code

    # noinspection PyUnusedLocal
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
        return self.action_log[:]

    def printActionLog(self):
        self.logAdd("====== TEST " + self.getName() + " ACTION LOG: ======")
        for act in self.action_log:
            self.logAdd("    " + act.serializeAction())
        self.logAdd("=" * 20)

    def logStart(self):
        try:
            create_log_dir(self.log_dir)
            logFile = open(self.log_file, "w")
            logText = "[" + self.test_name + " log start on " + self.base_url + "]\n"
            logFile.write(logText.encode("UTF-8"))
            logFile.close()
            # indicate that log was already created
            self.log_started = True
            self.log_time = current_time()
        except IOError:
            self.fatalTest("Cannot create log file " + userSerialize(self.log_file) + ". ")

    def setCloseOnExit(self, flag):
        self.m_closeOnExit = flag

    # PHP errors auto-check toggle
    def setAutoPhpErrorChecking(self, checkErrors=True):
        self.check_errors = checkErrors

    def set404Checking(self, value=True):
        if value:
            self.logAdd("Enabling 404 checking. ")
        else:
            self.logAdd("Disabling 404 checking. ")
        self.do_check_404 = value

    def setPhpErrorsAsWarnings(self, errorsAsWarnings=True):
        self.errors_as_warnings = errorsAsWarnings

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
        fullUrl = self.base_url + normUrl
        return self.gotoSite(fullUrl, comment)

    def lastActionType(self):
        if self.action_log:
            return self.action_log[-1].m_action
        return "none"

    # @comment usually means link name (or id), which we used to navigate to this URL.
    def gotoSite(self, fullUrl, comment=""):
        actionMsg = "Link: " + userSerialize(fullUrl)
        if not isVoid(comment):
            actionMsg += (" comment: " + userSerialize(comment) + " ")
        self.addAction("navigate", actionMsg)
        self.m_driver.get(fullUrl)
        self.check_page_errors()
        self.check404()

    def check_page_errors(self):
        if self.check_errors:
            self.assertPhpErrors()

    def check404(self):
        if not self.do_check_404:
            return
        if self.checkSourceTextPresent(self.text_on_page_404, negative=True):
            raise PageNotFound(
                "Requested URL '{}' leads to non-existing page (404). ".format(userSerialize(self.curUrl()))
            )

    def set404Text(self, text):
        self.text_on_page_404 = text

    def isBaseUrl(self, link):
        pfx_list = ["http://", "https://"]
        # short links without domain at all
        if not any([link.startswith(pfx) for pfx in pfx_list]):
            return True

        # seems that URL is full
        pure_base_url = self.base_url
        pure_link = link
        for pfx in pfx_list:

            pure_base_url = pure_base_url.replace(pfx, "", 1)
            pure_link = pure_link.replace(pfx, "", 1)

        if not pure_link.startswith(pure_base_url):
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
            exMsg = "Forbidden URL is found on the page in assertUrlNotPresent: " + userSerialize(
                linkName) + ". " + self.displayReason(reason)
            self.failTest(exMsg)
        except ItemNotFound:
            self.logAdd(u"URL " + userSerialize(linkName) + " is really not present (ItemNotFound exception raised). ")

    def assertPageNotPresent(self, pageUrl, reason=""):
        try:
            self.gotoPage(pageUrl)
            exMsg = "Forbidden page is found while going to URL in assertPageNotExists: " + userSerialize(
                pageUrl) + ". " + self.displayReason(reason)
            self.failTest(exMsg)
        except PageNotFound:
            self.logAdd(u"Page " + userSerialize(pageUrl) + " is really not present (PageNotFound exception raised). ")

    def assertUrlPresent(self, linkName, reason=""):
        try:
            self.getUrlByLinkText(linkName, reason=reason)
        except ItemNotFound:
            exceptionMessage = "Required URL is not found on the page in assertUrlPresent: " + userSerialize(
                linkName) + ". " + self.displayReason(reason)
            self.failTest(exceptionMessage)

    def wait(self, seconds, comment=""):
        log_comment_text = "Comment: " + userSerialize(comment) if comment else ""
        self.addAction("wait", "Waiting for " + userSerialize(seconds) + " seconds. " + log_comment_text)
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
            self.failTest("Checkbox with id '" + eleId + "' has improper value, expected " + userSerialize(
                boolValue) + ". " + self.displayReason(reason))

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
        self.addAction(
            "fill",
            "element name: " + userSerialize(name) + ", text: " + wrapIfLong(userSerialize(text)) + " "
        )
        self.getElementByName(name).send_keys(text)
        return get_value(self.getElementByName(name))

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
            return get_value(ele)
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
            "element: ACE, actual: " + wrapIfLong(userSerialize(currentText)) + ", expected: " + wrapIfLong(
                userSerialize(text)) + " "
        )
        return False

    def assertAceEditorElementText(self, text, reason=""):
        if not self.checkAceEditorElementText(text):
            self.failTest("ACE element text does not match expected: " + wrapIfLong(
                userSerialize(text)) + ". " + self.displayReason(reason))

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
            self.check_page_errors()
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by name '" + eleName + "'. ")

    # returns option value (index) and text
    def getOptionValueByIdAndIndex(self, eleId, index):
        """
        element index is started with 1, not 0.
        """
        if index < 1:
            self.fatalTest(
                "Invalid index in getOptionValueByIdAndIndex for element " + eleId + ". Index should be positive (1 and above). ")
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
        return get_value(oneOption), oneOption.text

    def getOptionValueByName(self, eleName):
        try:
            return get_value(self.getElementByName(eleName).find_element_by_xpath("option[@selected='selected']"))
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by name " + userSerialize(eleName) + ". ")

    def getOptionValueById(self, eleId):
        try:
            return get_value(self.getElementById(eleId).find_element_by_xpath("option[@selected='selected']"))
        except NoSuchElementException:
            self.failTest("Cannot get drop-down (select) element by id '" + eleId + "'. ")

    def getElementValueById(self, eleId):
        self.checkEmptyParam(eleId, "getElementValueById")
        self.addAction("get-value", "element id: '" + eleId + "'")
        return get_value(self.getElementById(eleId))

    def getElementValueByName(self, eleName):
        self.checkEmptyParam(eleName, "getElementValueByName")
        self.addAction("get-value", "element name: " + userSerialize(eleName) + " ")
        return get_value(self.getElementByName(eleName))

    def checkElementValueById(self, eleId, text):
        self.checkEmptyParam(eleId, "checkElementValueById")
        self.addAction(
            "check-value",
            "element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". "
        )
        eleValue = get_value(self.getElementById(eleId))
        if not eleValue:
            self.logAdd("None 'value' in element id '" + eleId + "'. Maybe it has no attribute 'value'?", "warning")
            return False
        self.logAdd("checkElementValueById: current element '" + eleId + "' value is: " + wrapIfLong(
            userSerialize(eleValue)) + ". ")
        if isEqual(eleValue, text):
            self.logAdd(
                "check-value:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
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
        self.logAdd("checkElementTextById: current element '" + eleId + "', text is: " + wrapIfLong(
            userSerialize(eleText)) + ". ")
        if isEqual(eleText, text):
            self.logAdd(
                "check-text:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
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
        self.logAdd("checkElementSubTextById: current element '" + eleId + "', text is: " + wrapIfLong(
            userSerialize(eleText)) + ". ")
        if text in eleText:
            self.logAdd(
                "check-subtext:ok, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
            return True
        self.logAdd(
            "check-subtext:fail, element id: '" + eleId + "', expected: " + wrapIfLong(userSerialize(text)) +
            ", actual: " + wrapIfLong(userSerialize(eleText)) + ". "
        )
        return False

    def assertElementSubTextById(self, eleId, text, reason=""):
        if not self.checkElementSubTextById(eleId, text):
            self.failTest(
                "Element with id '" + eleId + "' text does not contain expected: " + wrapIfLong(
                    userSerialize(text)) + ". " + self.displayReason(reason)
            )

    def checkElementValueByName(self, name, text):
        self.checkEmptyParam(name, "checkElementValueByName")
        self.addAction(
            "check-value",
            "element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) + ". "
        )
        eleValue = get_value(self.getElementByName(name))
        if not eleValue:
            self.logAdd("None 'value' in element named '" + name + "'. Maybe it has no attribute 'value'?", "warning")
            return False
        self.logAdd("checkElementValueByName: current element named '" + name + "' has value: " + wrapIfLong(
            userSerialize(eleValue)) + ". ")
        if isEqual(eleValue, text):
            self.logAdd(
                "check-value:ok, element name: '" + name + "', expected: " + wrapIfLong(userSerialize(text)) + ". ")
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
            self.failTest("Element with name '" + userSerialize(name) + " value does not match expected: " + wrapIfLong(
                userSerialize(text)) + ". ")

    def addAction(self, name, details=""):
        testAction = TestAction(name, details)
        self.action_log.append(TestAction(name, details))
        self.logAdd(testAction.serializeAction(), "action")

    def clickElementByName(self, name):
        self.addAction("click", "element name: " + userSerialize(name) + " ")
        self.getElementByName(name).click()
        self.check_page_errors()

    def doubeClickElementByName(self, name):
        self.addAction("double-click", "element name: '" + name + "'")
        actionChains = ActionChains(self.m_driver)
        actionChains.double_click(self.getElementByName(name)).perform()
        self.check_page_errors()

    def clickElementById(self, eleId):
        self.addAction("click", "element id: '" + eleId + "'")
        self.getElementById(eleId).click()
        self.check_page_errors()

    def doubeClickElementById(self, eleId):
        self.addAction("bouble-click", "element id: '" + eleId + "'")
        actionChains = ActionChains(self.m_driver)
        actionChains.double_click(self.getElementById(eleId)).perform()
        self.check_page_errors()

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
            self.log_check_stop_words = stopList
        else:
            self.log_check_stop_words = [stopList]

    def isStopWord(self, text):
        return text in self.log_check_stop_words or text == self.text_on_page_404

    def checkTextPresent(self, xpath, text, option_list=None, negative=False):
        option_list = option_list or []

        self.checkEmptyParam(xpath, "checkTextPresent")
        self.checkEmptyParam(text, "checkTextPresent")

        count = 0
        wait_time = 0.0
        max_retries = MAX_RETRIES if not negative else MAX_RETRIES_NEGATIVE
        while count < max_retries:
            self.wait(wait_time, u"Checking for text '" + userSerialize(text) + u"'")
            count += 1
            wait_time += TIME_INC
            try:
                is_found = self.check_text_present_once(xpath, text, option_list)
                if is_found:
                    return True
                logging.debug("checkTextPresent(): expected text not found, retrying.")
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

    def checkSourceTextPresent(self, text, option_list=None, negative=False):
        option_list = option_list or []
        self.checkEmptyParam(text, "checkSourceTextPresent")

        count = 0
        wait_time = 0.0
        max_retries = MAX_RETRIES if not negative else MAX_RETRIES_NEGATIVE
        while count < max_retries:
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

    def assert_equal(self, got_value, expected_value, error_text):
        if got_value != expected_value:
            error_text += "Expected '{0}', got '{1}'.".format(expected_value, got_value)
            logging.error("TEST FAILED: %s", userSerialize(error_text))
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
        if self.checkTextPresent(xpath, text, negative=True):
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
        if self.checkSourceTextPresent(text, negative=True):
            errText = "Forbidden text " + userSerialize(text) + " found on page " + userSerialize(
                self.curUrl()) + ". " + self.displayReason(reason)
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
                msg = "Cannot find URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(
                    self.curUrl()) + ". " + self.displayReason(reason)
                self.throwItemNotFound(msg, option_list=option_list)

    def countIndexedUrlsByLinkText(self, urlText, sibling=""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling = "text()"

            xpath = "//a[" + sibling + "='" + urlText + "']"
            urls = self.m_driver.find_elements_by_xpath(xpath)

            if not isList(urls):
                self.fatalTest(
                    "countIndexedUrlsByLinkText(): Something bad retrieved from find_elements_by_xpath: "
                    "it's not a list of WebElement. "
                )

            listSize = len(urls)
            self.logAdd("Urls list size: " + userSerialize(listSize))
            return listSize
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(
                self.curUrl()) + ". "
            self.throwItemNotFound(msg)

    def gotoIndexedUrlByLinkText(self, urlText, index, sibling=""):
        # case: <a><span>text</span></a> is not captured by internal of 'gotoUrlByLinkText'
        try:
            if isVoid(sibling):
                sibling = "text()"

            xpath = "//a[" + sibling + "='" + urlText + "']"
            urls = self.m_driver.find_elements_by_xpath(xpath)

            if not isList(urls):
                self.fatalTest(
                    "clickIndexedElementByText(): Something bad retrieved from find_elements_by_xpath: "
                    "it's not a list of WebElement. "
                )

            self.logAdd("Urls list size: " + userSerialize(len(urls)))
            if index < len(urls):
                url = urls[index]
                href = url.get_attribute("href")
                self.logAdd("Found URL with index " + userSerialize(index) + ": " + href)
                if isVoid(href):
                    self.fatalTest(
                        "clickIndexedElementByText(): empty 'href' attribute of a-element with index " + userSerialize(
                            index)
                    )
                self.gotoSite(href)
            else:
                self.failTest(
                    "No index '" + userSerialize(index) + "' in URL array with link text " +
                    userSerialize(urlText) + " on page " + userSerialize(self.curUrl()) + ". "
                )
        except NoSuchElementException:
            # here we don't use failTest() because this special exception is caught in assertUrlNotPresent, etc.
            msg = "Cannot find no one URL by link text: " + userSerialize(urlText) + " on page " + userSerialize(
                self.curUrl()) + ". "
            self.throwItemNotFound(msg)

    def logAdd(self, text, logLevel="debug"):
        try:
            if not self.log_started:
                self.logStart()

            newTime = current_time()
            duration = newTime - self.log_time
            self.log_time = newTime
            fullLogText = u"[{level:8}][{dur:06.2f}]: ".format(level=logLevel, dur=duration) + text.strip()
            print fullLogText.encode("UTF-8")
            logFile = open(self.log_file, 'a')
            logFile.write((fullLogText + "\n").encode("UTF-8"))
            logFile.close()
        except IOError:
            self.fatalTest("Cannot write message to log file " + userSerialize(self.log_file) + ". ")

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
                self.logAdd(
                    "PHP ERROR " + userSerialize(word) + " detected on page " + userSerialize(self.curUrl()) + ": ")
                self.logAdd("ERROR_PAGE_BEGIN =================")
                self.logAdd(pageText)
                self.logAdd("ERROR_PAGE_END ===================")
                return True, word
        return False, None

    def assertPhpErrors(self):
        checkResult, suspWord = self.checkPhpErrors()
        if checkResult:
            logMsg = "PHP ERROR " + userSerialize(suspWord) + " detected on the page " + userSerialize(
                self.curUrl()) + ". "
            self.logAdd(logMsg, "warning")
            if not self.errors_as_warnings:
                raise TestError(logMsg)
