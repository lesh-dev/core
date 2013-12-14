#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap, time
from xtest_config import XcmsTestConfig

class XcmsAuthAddNewUser(xtest_common.XcmsTest):
    """
    This test checks user add functional.
    It does following steps:
    * login as root user
    * navigate to user control panes
    * add random user
    * login as new user
    * change user password
    * logout
    * login with incorrect password
    * change password
    * login again with changed password
    """

    def run(self):
#       self.drv().getEval("window.resizeTo(X, Y); window.moveTo(0,0);")
        conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(conf.getPhpErrorCheckFlag())

        xtest_common.assertNoInstallerPage(self)


        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())

        self.gotoRoot()


        # first, login as admin
        inpLogin = "an_test_user_" + random_crap.randomText(8)
        inpEMail = random_crap.randomEmail()
        inpPass = random_crap.randomText(10)
        inpName = u"Вася Пупкин" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = xtest_common.createNewUser(self, conf, inpLogin, inpEMail, inpPass, inpName)

        print "logging as created user. "
        if not xtest_common.performLogin(self, inpLogin, inpPass):
            raise selenium_test.TestError("Cannot login as newly created user. ")

        # logout self
        xtest_common.performLogoutFromSite(self)

        # test wrong auth
        print "logging as created user with incorrect password "
        if xtest_common.performLogin(self, inpLogin, "wrong_pass" + inpPass):
            raise selenium_test.TestError("I'm able to login with incorrect password. Auth is broken. ")

#       self.assertBodyTextPresent(u"Пароль всё ещё неверный"); already checked inside

        # and now, test bug with remaining cookies:
        # we navigate to root page, and see auth panel!
        print "logging again as created user. "
        if not xtest_common.performLogin(self, inpLogin, inpPass):
            raise selenium_test.TestError("Cannot login again as newly created user. ")

        xtest_common.gotoCabinet(self)

        # let's try to change password.
        self.gotoUrlByLinkText(u"Сменить пароль")

        newPass = inpPass + "_new"
        self.fillElementById("old_passwd-input", inpPass)
        newPass1 = self.fillElementById("new_passwd-input", newPass)
        newPass2 = self.fillElementById("new_passwd_confirm-input", newPass)
        if newPass1 != newPass2:
            raise RuntimeError("Unpredicted input behavior on password change")
        newPass = newPass1
        self.clickElementByName("change_my_password")
        self.assertBodyTextPresent(u"Пароль успешно изменён")

        xtest_common.performLogoutFromAdminPanel(self)

        print "logging again as created user with new password"
        if not xtest_common.performLogin(self, inpLogin, newPass):
            raise selenium_test.TestError("Cannot login again as newly created user with changed password. ")

        # logout self
        xtest_common.performLogoutFromSite(self)

        # and now let's edit user profile.

        print "now let's edit profile. Logging 3-rd time with new password"
        if not xtest_common.performLogin(self, inpLogin, newPass):
            raise selenium_test.TestError("Cannot login again for profile info change. ")

        xtest_common.gotoCabinet(self)
        # navigate to user profile which is just user login
        # TODO: BUG, make separate links

        self.gotoUrlByPartialLinkText(inpLogin)
        self.assertBodyTextPresent(u"Привет, " + inpLogin)

        nameEle = "name-input"
        emailEle = "email-input"

        currentDisplayName = self.getElementValueById(nameEle)
        if currentDisplayName != inpName:
            raise selenium_test.TestError("Display name in user profile does not match name entered on user creation. Expected: '" + inpName + "', got '" + currentDisplayName + "'. ")

        currentEMail = self.getElementValueById(emailEle)
        if currentEMail != inpEMail:
            raise selenium_test.TestError("User e-mail in user profile does not match e-mail entered on user creation. Expected: '" + inpEMail + "', got '" + currentEMail + "'. ")

        newName = u"Петя Иванов" + random_crap.randomText(6)
        newEMail = random_crap.randomEmail()

        newName = self.fillElementById(nameEle, newName)

        print "New user display name is ", newName
        newEMail = self.fillElementById(emailEle, newEMail)
        print "New user e-mail is ", newEMail

        self.clickElementByName("update_me")

        xtest_common.performLogoutFromAdminPanel(self)

        print "now let's login again and see updated profile."
        if not xtest_common.performLogin(self, inpLogin, newPass):
            raise selenium_test.TestError("Cannot login after profile info change. ")

        xtest_common.gotoCabinet(self)
        # navigate to user profile which is just user login
        self.gotoUrlByLinkText(inpLogin)
        self.assertBodyTextPresent(u"Привет, " + inpLogin)

        currentDisplayName = self.getElementValueById(nameEle)
        if currentDisplayName != newName:
            raise selenium_test.TestError("Display name in user profile does not match changed user name. Expected: '" + newName + "', got '" + currentDisplayName + "'. ")

        currentEMail = self.getElementValueById(emailEle)
        if currentEMail != newEMail:
            raise selenium_test.TestError("User e-mail in user profile does not match changed user e-mail. Expected: '" + newEMail + "', got '" + currentEMail + "'. ")




