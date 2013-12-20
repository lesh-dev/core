#!/usr/bin/python
# -*- coding: utf8 -*-

#from selenium import webdriver
import sys, time

import selenium_test, random_crap
from xtest_config import XcmsTestConfig

class XcmsBaseTest(selenium_test.SeleniumTest):
    # override base error-checking method
    def checkPageErrors(self):
        super(XcmsTest, self).checkPageErrors()
        source = self.getPageSource()
        stoppers = ["<!#", "#!>"]
        for stopper in stoppers:
            if stopper in source:
                self.failTest("Forbidden crap '" + stopper + "' found on page. ")
    
class XcmsTest(XcmsBaseTest):
    def init(self):
        super(XcmsTest, self).init()

        self.m_conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(self.m_conf.getPhpErrorCheckFlag())
        xtest_common.assertNoInstallerPage(self)
        #xtest_common.setTestNotifications(self, self.m_conf.getNotifyEmail(), self.m_conf.getAdminLogin(), self.m_conf.getAdminPass())
        
    def getAdminLogin(self):
        return self.m_conf.getAdminLogin()

    def getAdminPass(self):
        return self.m_conf.getAdminPass()
        
    
def isInstallerPage(test):
    return test.curUrl().endswith("install.php")

def assertNoInstallerPage(test):
    test.gotoRoot()
    if isInstallerPage(test):
        test.failTest("Installer page detected, while we did not expected it. You should run this test on installed XCMS. ")

def gotoAuthLink(test):
    test.logAdd("xtest_common.gotoAuthLink: going to authenticate. ")
    test.gotoUrlByLinkText(u"Авторизация")

def gotoAdminPanel(test):
    test.logAdd("xtest_common.gotoAdminPanel: going to admin control panel. ")
    test.gotoUrlByLinkText(u"Админка")

def gotoCabinet(test):
    test.logAdd("xtest_common.gotoCabinet: going to user control panel (cabinet). ")
    test.gotoUrlByLinkText(u"Личный кабинет")

def gotoAllPeople(test):
    test.logAdd("xtest_common.gotoAllPeople: going to 'All People' menu. ")
    test.gotoUrlByLinkText(u"Все люди")

def getAuthLink(test):
    return test.getUrlByLinkText(u"Авторизация")

def gotoBackToAnketaView(test):
    test.gotoUrlByLinkText(u"Вернуться к просмотру участника")

def gotoBackToPersonView(test):
    test.gotoUrlByLinkText(u"Вернуться к просмотру участника")

def gotoEditPerson(test):
    test.gotoUrlByLinkText(u"Редактировать анкетные данные")

def gotoBackAfterComment(test):
    #test.gotoUrlByLinkText(u"Вернуться к списку комментов") # older variant
    gotoBackToAnketaView(test)

def getAdminPanelLink(test):
    return test.getUrlByLinkText(u"Админка")

def performLogoutFromSite(test):
    test.gotoUrlByLinkText(u"Выход")

def performLogoutFromAdminPanel(test):
    test.gotoUrlByLinkText(u"Выйти")

def performLogin(test, login, password):
    """
    returns True if login was successful
    """
    if test is None:
        raise RuntimeError("Wrong webdriver parameter passed to performLogin. ")

    test.addAction("user-login", login + " / " + password)
#   test.logAdd("performLogin(" + login + ", " + password + ")")

    print "performLogin(): goto root"

    test.gotoRoot()

    # assert we have no shit cookies here
    test.assertUrlNotPresent(u"Админка", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")
    test.assertUrlNotPresent(u"Личный кабинет", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")

    gotoAuthLink(test)

    test.assertSourceTextPresent(u"Логин")
    test.assertSourceTextPresent(u"Пароль")
    test.assertSourceTextPresent(u"Требуется аутентификация")

    #<input type="text" name="auth-login" />
    #ele = test.drv().find_element_by_name("auth-login")
    test.fillElementById("auth-login", login)
    test.fillElementById("auth-password", password)

    test.clickElementById("auth-submit")

    wrongAuth = test.checkSourceTextPresent([u"Пароль всё ещё неверный", "Wrong password"])
    if wrongAuth:
        return False

    # now let's check that Cabinet link and Exit link are present. if not - it's a bug.

    test.assertUrlPresent(u"Выход", "Here should be logout link after successful authorization. ")
    test.assertUrlPresent(u"Личный кабинет", "Here should be Cabinet link after successful authorization. ")

    return True

def performLogout(test):
    print "performLogout()"
    test.addAction("user-logout")
    test.gotoPage("/?&mode=logout&ref=ladmin")

def performLoginAsAdmin(test, login, password):
    print "performLoginAsAdmin( login: " + login + ", password: " + password + " )"
    if not performLogin(test, login, password):
        print "Admin authorization failed"
        raise selenium_test.TestError("Cannot perform Admin authorization as " + login + "/" + password)

    print "performLoginAsAdmin(): checking admin panel link"

    #check that we have entered the CP.
    # just chech that link exists.
    cpUrl = getAdminPanelLink(test)
    #test.gotoSite(cpUrl)


def createNewUser(test, conf, login, email, password, name, auxParams = []):
    print "createNewUser( login: " + login + "', email: " + email + ", password: " + password + ", name: " + name + " )"

    if not "do_not_login_as_admin" in auxParams:
        performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
        gotoAdminPanel(test)

    gotoUserList(test)

    test.gotoUrlByLinkText(["Create user", u"Создать пользователя"])

    inpLogin = test.fillElementById("login", login)
    print "login = '" + inpLogin + "'"
    if inpLogin == "":
        raise RuntimeError("Filled login value is empty!")

    inpEMail = test.fillElementById("email", email)
    inpPass1 = test.fillElementById("password", password)
    print "original pass: '" + password + "'"
    inpPass2 = test.fillElementById("password_confirm", password)
    if inpPass1 != inpPass2:
        raise RuntimeError("Unpredicted input behavior on password entering")
    inpPass = inpPass1
    print "actual pass: '" + inpPass + "'"

    inpName = test.fillElementById("name", name)

    # set notify checkbox.
    # test.clickElementById("notify_user-checkbox")
    # send form

    test.clickElementByName("create_user")


    if "do_not_validate" in auxParams:
        print "not validating created user, just click create button and shut up. "
        return inpLogin, inpEMail, inpPass, inpName

    print "user created, going to user list again to refresh. "

    test.assertBodyTextPresent(u"Пользователь '" + inpLogin + u"' успешно создан")
    # refresh user list
    test.gotoUrlByLinkText(u"Пользователи")

    # enter user profile
    print "entering user profile. "

    profileLink = inpLogin
    # TODO, SITE BUG: make two separate links
    test.gotoUrlByPartialLinkText(profileLink)

    test.assertBodyTextPresent(u"Учётные данные")
    test.assertBodyTextPresent(u"Привилегии")

    # temporary check method
    # test user login
    test.assertTextPresent("//div[@class='user-ops']", inpLogin)
    # test user creator (root)
    test.assertTextPresent("//div[@class='user-ops']", conf.getAdminLogin())
    test.assertElementValueById("name-input", inpName)
    test.assertElementValueById("email-input", inpEMail)

    #logoff root
    if not "do_not_logout_admin" in auxParams:
        performLogout(test)

    return inpLogin, inpEMail, inpPass, inpName

# set email to user (by admin panel)
def setUserEmailByAdmin(test, conf, login, email, auxParams = []):
    print "setEmailToUserByAdmin( login: " + login + "', email: " + email + " )"
    
    test.logAdd("xtest_common.setUserEmailByAdmin: updating email for user '" + login + "' to '" + email + ". ")

    if not "do_not_login_as_admin" in auxParams:
        performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
        gotoAdminPanel(test)

    gotoUserList(test)

    test.gotoUrlByPartialLinkText(login)

    inpEMail = test.fillElementById("email-input", email)
    test.clickElementByName("update_user")

    #logoff root
    if not "do_not_logout_admin" in auxParams:
        performLogout(test)


def addCommentToPerson(test):
    test.gotoUrlByLinkText(u"Добавить комментарий")
    commentText = random_crap.randomText(40) + "\n" + random_crap.randomText(50) + "\n" + random_crap.randomText(30)

    commentText = test.fillElementByName("comment_text", commentText)

    test.clickElementByName("update-person_comment")
    test.assertBodyTextPresent(u"Комментарий успешно сохранён")
    gotoBackToAnketaView(test)
    return commentText

def editCommentToPerson(test, commentLinkId):
    test.gotoUrlByLinkId("comment-edit-1")
    oldCommentText = test.getElementValueByName("comment_text")
    newCommentText =  random_crap.randomText(10) + "\n" + oldCommentText + "\n" + random_crap.randomText(6)
    newCommentText = test.fillElementByName("comment_text", newCommentText)
    test.clickElementByName("update-person_comment")
    test.assertBodyTextPresent(u"Комментарий успешно сохранён")
    gotoBackToAnketaView(test)
    return newCommentText

def setTestNotifications(test, emailString, adminLogin, adminPass):
    performLoginAsAdmin(test, adminLogin, adminPass)
    gotoAdminPanel(test)
    test.gotoUrlByLinkText(u"Уведомления")

    test.fillElementById("edtg_user-change", emailString);
    test.fillElementById("edtg_content-change", emailString);

    test.fillElementById("edtg_reg", emailString);

    test.fillElementById("edtg_reg-test", emailString);
    test.fillElementById("edtg_reg-managers", emailString);
    test.fillElementById("edtg_reg-managers-test", emailString);

    test.clickElementById("editTag")
    performLogout(test)

def shortAlias(last, first):
    return (last + " " + first).strip()

def fullAlias(last, first, mid):
    return (last + " " + first + " " + mid).strip()

def gotoUserList(test):
    test.logAdd("Navigating to user list from admin CP. ")
    test.gotoUrlByLinkText(u"Пользователи")
    test.assertBodyTextPresent(u"Администрирование пользователей")

def checkPersonAliasInPersonView(test, personAlias):
    test.assertElementTextById("person-title", personAlias)

