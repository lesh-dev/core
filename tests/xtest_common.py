#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test
import random_crap

from xtest_config import XcmsTestConfig


MAX_RETRIES = 4
TIME_INC = 0.05


class XcmsBaseTest(selenium_test.SeleniumTest):
    """
        Base test class wth advanced error checking"
    """
    # override base error-checking method
    def init(self):
        super(XcmsBaseTest, self).init()
        self.set404Text(u"Нет такой страницы")

    def check_page_errors(self):
        super(XcmsBaseTest, self).check_page_errors()
        source = self.getPageSource()
        stoppers = ["<!#", "#!>"]
        for stopper in stoppers:
            if stopper in source:
                self.failTest("Forbidden crap '" + stopper + "' found on page. ")

        self.check_doc_type()
        if self.is_auth_page() and self.lastActionType() == "navigate":
            self.logAdd("We are on the AUTH page. Seems that page access was denied. ", "warning")

    def is_auth_page(self):
        stop_phrases = [u"Требуется аутентификация", u"Пароль всё ещё неверный", u"Доступ запрещён"]
        return self.checkSourceTextPresent(stop_phrases, option_list=["silent"], negative=True)

    def check_doc_type(self):
        count = 0
        wait_time = 0.0
        while count < MAX_RETRIES:
            wait_time += TIME_INC
            count += 1
            self.wait(wait_time, "check_doc_type")
            if self.check_doc_type_once():
                return
            self.logAdd("DOCTYPE not detected, retrying")
        self.failTest("DOCTYPE directive not found on page {0}. ".format(self.curUrl()))

    def check_doc_type_once(self):
        first_line, source_block = self.get_page_source_first_line()
        if "<!DOCTYPE" in first_line:
            # ok
            return True

        # not found
        if self.is_auth_page():
            self.logAdd("DOCTYPE not detected, but this page seems to be Auth page. ", "warning")
            return True
        source_block = "\n".join(source_block)
        self.logAdd("Source beginning without DOCTYPE:\n" + source_block.strip())
        return False

    def get_page_source_first_line(self):
        source = self.getPageSource()
        newline_pos = source.find("\n")
        # self.logAdd("Newline found at {0}".format(newlinePos))
        return source[:newline_pos], source[:1000].split("\n")[:4]

    def is_installer_page(self):
        return self.curUrl().endswith("install.php")

    def assert_no_installer_page(self):
        self.gotoRoot()
        if self.is_installer_page():
            self.fatalTest(
                "Installer page detected, while we did not expected it. You should run this test on installed XCMS. "
            )

    def goto_alias(self, alias):
        self.logAdd("Going to the page via alias " + alias)
        self.gotoPage(alias)


class XcmsTestWithConfig(XcmsBaseTest):
    """
        generic Xcms test with config
    """
    m_conf = None

    def init(self):
        super(XcmsTestWithConfig, self).init()
        self.m_conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(self.m_conf.getPhpErrorCheckFlag())
        # self.maximizeWindow()

    def goto_rebuild_aliases(self):
        self.logAdd("Rebuilding aliases. ")
        self.gotoUrlByLinkText(u"Перестроить alias-ы")

    def gotoNotificationsPage(self):
        self.gotoUrlByLinkText(u"Уведомления")

    def gotoCreatePage(self, reason=""):
        self.gotoUrlByLinkText(u"Подстраница", reason)

    def gotoRemovePage(self, reason=""):
        self.gotoUrlByLinkText(u"Удалить", reason)

    def getAnketaPageHeader(self):
        return u"Анкета"

    def getUserListLinkName(self):
        return u"Пользователи"

    def setTestNotifications(self):

        emailString = self.m_conf.getNotifyEmail()

        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoNotificationsPage()

        self.fillElementById("edtg_user-change", emailString)
        self.fillElementById("edtg_content-change", emailString)

        self.fillElementById("edtg_reg", emailString)
        self.fillElementById("edtg_reg-managers", emailString)

        self.clickElementById("edit_tag-submit")
        self.performLogout()

    def checkTestNotifications(self):
        """
            check if test notification is set properly (it's done by 'publish testing' script).
        """

        emailString = self.m_conf.getNotifyEmail()

        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoNotificationsPage()

        reason = "Notifications were not set properly. "

        self.assertElementValueById("edtg_user-change", emailString, reason)
        self.assertElementValueById("edtg_content-change", emailString, reason)

        self.assertElementValueById("edtg_reg", emailString, reason)
        self.assertElementValueById("edtg_reg-managers", emailString, reason)

        self.performLogout()

    def performLoginAsEditor(self):
        return self.performLoginAsAdmin()

    def performLoginAsManager(self):
        return self.performLoginAsAdmin()

    def performLoginAsAdmin(self):
        login = self.getAdminLogin()
        password = self.getAdminPass()
        self.logAdd("performLoginAsAdmin")
        if not self.performLogin(login, password):
            self.logAdd("Admin authorization failed")
            self.failTest("Cannot perform Admin authorization as " + login + "/" + password)

        self.logAdd("performLoginAsAdmin(): checking admin panel link")

        # check that we have entered the CP.
        # just chech that link exists.
        self.get_admin_panel_link()
        # test.gotoSite(cpUrl)

    def performLogin(self, login, password):
        """
        returns True if login was successful
        """
        self.addAction("user-login", login + " / " + password)
    #   test.logAdd("performLogin(" + login + ", " + password + ")")

        self.logAdd("performLogin(): goto root")

        self.gotoRoot()

        # assert we have no shit cookies here
        expl_adm = (
            "Here should be no auth cookies. But they are. "
            "Otherwise, your test is buggy and you forgot to logout previous user. "
        )
        self.assertUrlNotPresent(self.admin_panel_link_name(), expl_adm)
        if self.getElementById("cabinet", fail=False):
            self.failTest(expl_adm)

        self.gotoAuthLink()

        self.assertSourceTextPresent(u"Логин")
        self.assertSourceTextPresent(u"Пароль")
        self.assertSourceTextPresent(u"Требуется аутентификация")

        self.fillElementById("auth-login-input", login)
        self.fillElementById("auth-password-input", password)

        self.clickElementById("auth-submit")

        wrong_auth = self.checkSourceTextPresent([u"Пароль всё ещё неверный", "Wrong password"], negative=True)
        if wrong_auth:
            return False

        # now let's check that Cabinet link and Exit link are present. if not - it's a bug.
        self.getElementById("logout")
        self.getElementById("cabinet")

        return True

    def getAdminLogin(self):
        return self.m_conf.getAdminLogin()

    def getAdminPass(self):
        if "test.fizlesh.ru" in self.base_url:
            with open("root_password", 'r') as f:
                passwd = f.readline()
            return passwd
        return self.m_conf.getAdminPass()

    def performLogout(self):
        self.logAdd("performLogout")
        self.addAction("user-logout")
        self.gotoPage("/?&mode=logout&ref=admin")

    def ensure_logged_off(self):
        self.performLogout()
        self.gotoRoot()

    def getWelcomeMessage(self, login):
        return u"Привет, " + login

    def admin_panel_link_name(self):
        return u"Админка"

    def get_news_link_name(self):
        return u"Новости"

    def get_contacts_link_name(self):
        return u"Контакты"

    def get_admin_panel_link(self):
        return self.getElementById("admin")

    def gotoAuthLink(self):
        self.logAdd("gotoAuthLink: going to authenticate. ")
        self.clickElementById("signin")

    def getAuthLink(self):
        return self.getElementById("signin")

    def gotoAdminPanel(self):
        self.logAdd("gotoAdminPanel: going to admin control panel. ")
        self.gotoUrlByLinkId("admin")

    def getPersonAbsenceMessage(self):
        # return u"На " + self.m_conf.getTestSchoolName() + u" не присутствовал"
        return u"На данной школе не присутствовал"


class XcmsTest(XcmsTestWithConfig):
    """
        Generic XCMS test
    """
    def init(self):
        super(XcmsTest, self).init()
        self.assert_no_installer_page()

    """def createNewUser(self, login, email, password, name, aux_params=None):
        user_aux_params = aux_params or []
        logging.info(
            "createNewUser(login: '%s', email: '%s', password: '%s', name: '%s')", login, email, password, name
        )

        if "do_not_login_as_admin" not in user_aux_params:
            self.performLoginAsAdmin()
            self.gotoAdminPanel()

        self.gotoUserList()

        self.gotoUrlByLinkText(["Create user", u"Создать пользователя"])

        inp_login = self.fillElementById("login-input", login)
        self.logAdd("login = '" + inp_login + "'")
        if inp_login == "":
            raise RuntimeError("Filled login value is empty!")

        inpEMail = self.fillElementById("email-input", email)
        inpPass1 = self.fillElementById("password-input", password)
        self.logAdd("original pass: '{0}'".format(password))
        inpPass2 = self.fillElementById("password_confirm-input", password)
        if inpPass1 != inpPass2:
            raise RuntimeError("Unpredicted input behavior on password entering")
        inpPass = inpPass1
        self.logAdd("actual pass: '" + inpPass + "'")

        inpName = self.fillElementById("name-input", name)

        # set notify checkbox.
        # self.clickElementById("notify_user-checkbox")
        # send form

        if "manager_rights" in user_aux_params:
            self.logAdd("Setting manager rights for user. ")
            # set manager access level
            self.clickElementById("group_ank-checkbox")

        self.clickElementByName("create_user")

        if "do_not_validate" in user_aux_params:
            self.logAdd("not validating created user, just click create button and shut up. ")
            return inp_login, inpEMail, inpPass, inpName

        self.logAdd("user created, going to user list again to refresh. ")

        self.assertBodyTextPresent(u"Пользователь '" + inp_login + u"' успешно создан")

        # refresh user list (re-navigate to user list)
        self.gotoUserList()

        # enter user profile
        self.logAdd("entering user profile. ")

        profileLink = inp_login
        # TODO, SITE BUG: make two separate links
        self.gotoUrlByPartialLinkText(profileLink)

        self.assertBodyTextPresent(u"Учётные данные")
        self.assertBodyTextPresent(u"Привилегии")

        # temporary check method
        # test user login
        self.assertTextPresent("//div[@class='user-ops']", inp_login)
        # test user creator (root)
        self.assertTextPresent("//div[@class='user-ops']", self.m_conf.getAdminLogin())
        self.assertElementValueById("name-input", inpName)
        self.assertElementValueById("email-input", inpEMail)

        # logoff root
        if "do_not_logout_admin" not in user_aux_params:
            self.performLogout()

        return inp_login, inpEMail, inpPass, inpName"""

    def removePreviousUsersWithTestEmail(self, emailToDelete):
        self.performLoginAsAdmin()
        self.gotoAdminPanel()
        self.gotoUserList()

        while True:
            try:
                userUrl = self.getUrlByLinkText(emailToDelete, ["partial"])
                self.logAdd("Test user found, removing it. ")
                self.gotoSite(userUrl)
                self.clickElementById("check_delete_user")
                self.assertBodyTextPresent(u"Вы точно уверены, что хотите удалить этого пользователя?")
                self.clickElementById("delete_user")
                self.assertBodyTextPresent(u"Пользователь удалён.")

            except selenium_test.ItemNotFound:
                self.logAdd("Users with test email not found, continuing. ")
                break

        self.logAdd("Test users (old crap) removed, logging out. ")
        self.performLogoutFromAdminPanel()

    def setUserEmailByAdmin(self, login, email, auxParams=list()):
        """
            Set email to user (by admin panel)
        """
        self.logAdd("setEmailToUserByAdmin( login: " + login + "', email: " + email + " )")

        self.logAdd("setUserEmailByAdmin: updating email for user '" + login + "' to '" + email + ". ")

        if "do_not_login_as_admin" not in auxParams:
            self.performLoginAsAdmin()
            self.gotoAdminPanel()

        self.gotoUserList()

        self.gotoUrlByPartialLinkText(login)

        self.fillElementById("email-input", email)
        self.clickElementByName("update_user")

        # logoff root
        if "do_not_logout_admin" not in auxParams:
            self.performLogout()

    def gotoCabinet(self):
        self.logAdd("gotoCabinet: going to user control panel (cabinet). ")
        self.gotoUrlByLinkId("cabinet")

    def gotoEditPerson(self):
        # self.gotoUrlByLinkText(u"Редактировать анкетные данные")
        self.gotoUrlByLinkText(u"Ред.")

    def gotoBackAfterComment(self):
        # self.gotoUrlByLinkText(u"Вернуться к списку комментов") # older variant
        self.goto_back_to_anketa_view()

    def performLogoutFromSite(self):
        self.gotoUrlByLinkId("logout")

    def performLogoutFromAdminPanel(self):
        self.gotoUrlByLinkId("logout")

    def closeAdminPanel(self):
        self.gotoUrlByLinkText("X")

    def assertSitePageHeader(self, header, reason="Page header does not match expected. "):
        self.assertElementTextById("content-header", header, reason=reason)

    def editCommentToPerson(self, commentLinkId):
        self.gotoUrlByLinkId(commentLinkId)
        oldCommentText = self.getElementValueByName("comment_text")
        newCommentText = random_crap.random_text(10) + "\n" + oldCommentText + "\n" + random_crap.random_text(6)
        newCommentText = self.fillElementByName("comment_text", newCommentText)
        self.clickElementByName("update-person_comment")
        self.assertBodyTextPresent(u"Комментарий успешно сохранён")
        self.goto_back_to_anketa_view()
        return newCommentText

    def gotoUserList(self):
        self.logAdd("Navigating to user list from admin CP. ")
        self.gotoUrlByLinkText(self.getUserListLinkName())
        self.assertBodyTextPresent(u"Администрирование пользователей")

    def checkPersonAliasInPersonView(self, personAlias, reason=""):
        self.assertElementTextById("person-title", personAlias, reason)

    def getEditPageInPlaceLinkName(self):
        return u"Редактировать"

    def getEntranceLinkName(self):
        return u"Поступление"

    def gotoEditPageInPlace(self):
        self.gotoUrlByLinkText(self.getEditPageInPlaceLinkName())

    def gotoCloseEditor(self):
        self.logAdd("gotoCloseEditor")
        self.gotoUrlByLinkText(u"Свернуть редактор")

    def getAnketaListMenuName(self):
        return u"Анкеты"

    def checkScreenIsAdmin(self):
        screen = self.getElementTextById("screen")
        self.assert_equal(screen, u"Админка", "We are not in the admin panel. Cannot add new page. ")

    def addNewPage(self, parentPage, sysName, menuTitle, pageHeader, pageAlias):
        self.checkScreenIsAdmin()

        self.gotoUrlByLinkText(parentPage)
        self.gotoCreatePage()

        sysName = self.fillElementById("create-name-input", sysName)
        menuTitle = self.fillElementById("menu-title-input", menuTitle)
        pageHeader = self.fillElementById("header-input", pageHeader)
        pageAlias = self.fillElementById("alias-input", pageAlias)

        defaultPageType = self.getOptionValueById("create-pagetype-selector")
        if defaultPageType != "content":
            self.failTest("Default selected page type is not 'content': " + defaultPageType)

        self.clickElementById("create-page-submit")
        return sysName, menuTitle, pageHeader, pageAlias
