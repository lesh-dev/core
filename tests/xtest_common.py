#!/usr/bin/python
# -*- coding: utf8 -*-

#from selenium import webdriver
import sys, time

import selenium_test, random_crap
from xtest_config import XcmsTestConfig

class XcmsBaseTest(selenium_test.SeleniumTest):
    """
        Base test class wth advanced error checking"
    """
    # override base error-checking method
    def checkPageErrors(self):
        super(XcmsBaseTest, self).checkPageErrors()
        source = self.getPageSource()
        stoppers = ["<!#", "#!>"]
        for stopper in stoppers:
            if stopper in source:
                self.failTest("Forbidden crap '" + stopper + "' found on page. ")
                
    def isInstallerPage(self):
        return self.curUrl().endswith("install.php")

    def assertNoInstallerPage(self):
        self.gotoRoot()
        if self.isInstallerPage():
            self.failTest("Installer page detected, while we did not expected it. You should run this test on installed XCMS. ")
                

class XcmsTestWithConfig(XcmsBaseTest):
    """
        generic Xcms test with config
    """
    def init(self):
        print "XcmsTestWithConfig init"
        
        super(XcmsTestWithConfig, self).init()
        self.m_conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(self.m_conf.getPhpErrorCheckFlag())
        self.maximizeWindow()
        
    def setTestNotifications(self):
        
        emailString = self.m_conf.getNotifyEmail()
        
        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUrlByLinkText(u"Уведомления")

        self.fillElementById("edtg_user-change", emailString);
        self.fillElementById("edtg_content-change", emailString);

        self.fillElementById("edtg_reg", emailString);

        self.fillElementById("edtg_reg-test", emailString);
        self.fillElementById("edtg_reg-managers", emailString);
        self.fillElementById("edtg_reg-managers-test", emailString);

        self.clickElementById("editTag")
        self.performLogout()

    def checkTestNotifications(self):
        """
            check if test notification is set properly (it's done by 'publish testing' script).
        """
        
        emailString = self.m_conf.getNotifyEmail()
        
        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUrlByLinkText(u"Уведомления")

        reason = "Notifications were not set properly. "
        
        self.assertElementValueById("edtg_user-change", emailString, reason)
        self.assertElementValueById("edtg_content-change", emailString, reason)

        self.assertElementValueById("edtg_reg", emailString, reason)

        self.assertElementValueById("edtg_reg-test", emailString, reason)
        self.assertElementValueById("edtg_reg-managers", emailString, reason)
        self.assertElementValueById("edtg_reg-managers-test", emailString, reason)

        self.performLogout()
        
    def performLoginAsAdmin(self):
        login = self.getAdminLogin()
        password = self.getAdminPass()
        self.logAdd("performLoginAsAdmin")
        if not self.performLogin(login, password):
            self.logAdd("Admin authorization failed")
            self.failTest("Cannot perform Admin authorization as " + login + "/" + password)

        self.logAdd("performLoginAsAdmin(): checking admin panel link")

        #check that we have entered the CP.
        # just chech that link exists.
        cpUrl = self.getAdminPanelLink()
        #test.gotoSite(cpUrl)
    
    def performLogin(self, login, password):
        """
        returns True if login was successful
        """
        self.addAction("user-login", login + " / " + password)
    #   test.logAdd("performLogin(" + login + ", " + password + ")")

        print "performLogin(): goto root"

        self.gotoRoot()

        # assert we have no shit cookies here
        self.assertUrlNotPresent(u"Админка", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")
        self.assertUrlNotPresent(u"Личный кабинет", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")

        self.gotoAuthLink()

        self.assertSourceTextPresent(u"Логин")
        self.assertSourceTextPresent(u"Пароль")
        self.assertSourceTextPresent(u"Требуется аутентификация")

        #<input type="text" name="auth-login" />
        #ele = test.drv().find_element_by_name("auth-login")
        self.fillElementById("auth-login", login)
        self.fillElementById("auth-password", password)

        self.clickElementById("auth-submit")

        wrongAuth = self.checkSourceTextPresent([u"Пароль всё ещё неверный", "Wrong password"])
        if wrongAuth:
            return False

        # now let's check that Cabinet link and Exit link are present. if not - it's a bug.

        self.assertUrlPresent(u"Выход", "Here should be logout link after successful authorization. ")
        self.assertUrlPresent(u"Личный кабинет", "Here should be Cabinet link after successful authorization. ")

        return True
    
    def getAdminLogin(self):
        return self.m_conf.getAdminLogin()

    def getAdminPass(self):
        return self.m_conf.getAdminPass()
    
    def performLogout(self):
        self.logAdd("performLogout")
        self.addAction("user-logout")
        self.gotoPage("/?&mode=logout&ref=ladmin")

    
    def getAdminPanelLink(self):
        return self.getUrlByLinkText(u"Админка")
    
    def gotoAuthLink(self):
        self.logAdd("gotoAuthLink: going to authenticate. ")
        self.gotoUrlByLinkText(u"Авторизация")

    def getAuthLink(self):
        return self.getUrlByLinkText(u"Авторизация")

    def gotoAdminPanel(self):
        self.logAdd("gotoAdminPanel: going to admin control panel. ")
        self.gotoUrlByLinkText(u"Админка")
        
        
    
class XcmsTest(XcmsTestWithConfig):
    """
        generic Xcms test
    """
    def init(self):
        print "XcmsTest init"
        super(XcmsTest, self).init()
        # 
        self.assertNoInstallerPage()
        #xtest_common.setTestNotifications(self, self.m_conf.getNotifyEmail(), self.m_conf.getAdminLogin(), self.m_conf.getAdminPass())
            
    def createNewUser(self, login, email, password, name, auxParams = []):
        self.logAdd("createNewUser( login: " + login + "', email: " + email + ", password: " + password + ", name: " + name + " )")

        if not "do_not_login_as_admin" in auxParams:
            self.performLoginAsAdmin()
            self.gotoAdminPanel()

        self.gotoUserList()

        self.gotoUrlByLinkText(["Create user", u"Создать пользователя"])

        inpLogin = self.fillElementById("login", login)
        print "login = '" + inpLogin + "'"
        if inpLogin == "":
            raise RuntimeError("Filled login value is empty!")

        inpEMail = self.fillElementById("email", email)
        inpPass1 = self.fillElementById("password", password)
        print "original pass: '" + password + "'"
        inpPass2 = self.fillElementById("password_confirm", password)
        if inpPass1 != inpPass2:
            raise RuntimeError("Unpredicted input behavior on password entering")
        inpPass = inpPass1
        print "actual pass: '" + inpPass + "'"

        inpName = self.fillElementById("name", name)

        # set notify checkbox.
        # self.clickElementById("notify_user-checkbox")
        # send form

        self.clickElementByName("create_user")


        if "do_not_validate" in auxParams:
            print "not validating created user, just click create button and shut up. "
            return inpLogin, inpEMail, inpPass, inpName

        print "user created, going to user list again to refresh. "

        self.assertBodyTextPresent(u"Пользователь '" + inpLogin + u"' успешно создан")
        # refresh user list
        self.gotoUrlByLinkText(u"Пользователи")

        # enter user profile
        print "entering user profile. "

        profileLink = inpLogin
        # TODO, SITE BUG: make two separate links
        self.gotoUrlByPartialLinkText(profileLink)

        self.assertBodyTextPresent(u"Учётные данные")
        self.assertBodyTextPresent(u"Привилегии")

        # temporary check method
        # test user login
        self.assertTextPresent("//div[@class='user-ops']", inpLogin)
        # test user creator (root)
        self.assertTextPresent("//div[@class='user-ops']", self.m_conf.getAdminLogin())
        self.assertElementValueById("name-input", inpName)
        self.assertElementValueById("email-input", inpEMail)

        #logoff root
        if not "do_not_logout_admin" in auxParams:
            self.performLogout()

        return inpLogin, inpEMail, inpPass, inpName

    # set email to user (by admin panel)
    def setUserEmailByAdmin(self, login, email, auxParams = []):
        print "setEmailToUserByAdmin( login: " + login + "', email: " + email + " )"
        
        self.logAdd("setUserEmailByAdmin: updating email for user '" + login + "' to '" + email + ". ")

        if not "do_not_login_as_admin" in auxParams:
            self.performLoginAsAdmin()
            self.gotoAdminPanel()

        self.gotoUserList()

        self.gotoUrlByPartialLinkText(login)

        inpEMail = self.fillElementById("email-input", email)
        self.clickElementByName("update_user")

        #logoff root
        if not "do_not_logout_admin" in auxParams:
            self.performLogout()
    
    def gotoCabinet(self):
        self.logAdd("gotoCabinet: going to user control panel (cabinet). ")
        self.gotoUrlByLinkText(u"Личный кабинет")

    def gotoAllPeople(self):
        self.logAdd("gotoAllPeople: going to 'All People' menu. ")
        self.gotoUrlByLinkText(u"Все люди")


    def gotoBackToAnketaView(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру участника")

    def gotoBackToPersonView(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру участника")

    def gotoEditPerson(self):
        self.gotoUrlByLinkText(u"Редактировать анкетные данные")

    def gotoBackAfterComment(self):
        #self.gotoUrlByLinkText(u"Вернуться к списку комментов") # older variant
        self.gotoBackToAnketaView()

    def performLogoutFromSite(self):
        self.gotoUrlByLinkText(u"Выход")

    def performLogoutFromAdminPanel(self):
        self.gotoUrlByLinkText(u"Выйти")

    def addCommentToPerson(self):
        self.gotoUrlByLinkText(u"Добавить комментарий")
        commentText = random_crap.randomText(40) + "\n" + random_crap.randomText(50) + "\n" + random_crap.randomText(30)

        commentText = self.fillElementByName("comment_text", commentText)

        self.clickElementByName("update-person_comment")
        self.assertBodyTextPresent(u"Комментарий успешно сохранён")
        self.gotoBackToAnketaView()
        return commentText

    def editCommentToPerson(self, commentLinkId):
        self.gotoUrlByLinkId("comment-edit-1")
        oldCommentText = self.getElementValueByName("comment_text")
        newCommentText =  random_crap.randomText(10) + "\n" + oldCommentText + "\n" + random_crap.randomText(6)
        newCommentText = self.fillElementByName("comment_text", newCommentText)
        self.clickElementByName("update-person_comment")
        self.assertBodyTextPresent(u"Комментарий успешно сохранён")
        self.gotoBackToAnketaView()
        return newCommentText

    def gotoUserList(self):
        self.logAdd("Navigating to user list from admin CP. ")
        self.gotoUrlByLinkText(u"Пользователи")
        self.assertBodyTextPresent(u"Администрирование пользователей")

    def checkPersonAliasInPersonView(self, personAlias):
        self.assertElementTextById("person-title", personAlias)

def shortAlias(last, first):
    return (last + " " + first).strip()

def fullAlias(last, first, mid):
    return (last + " " + first + " " + mid).strip()


