#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap, time
from xtest_config import XcmsTestConfig

class XcmsAuthCheckDupLogin(xtest_common.XcmsTest):
    """
    add two users with identical logins.
    """

    def run(self):
        self.setAutoPhpErrorChecking(True)

        xtest_common.assertNoInstallerPage(self)

        conf = XcmsTestConfig()
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())

        # first, login as admin
        inpLogin = "dup_user_" + random_crap.randomText(8)
        inpEMail1 = random_crap.randomEmail()
        inpEMail2 = random_crap.randomEmail()
        inpPass1 = random_crap.randomText(10)
        inpPass2 = random_crap.randomText(10)
        inpName1 = u"Вася " + random_crap.randomText(6)
        inpName2 = u"Петя " + random_crap.randomText(6)

        inpLogin, inpEMail1, inpPass1, inpName1 = xtest_common.createNewUser(self, conf, inpLogin, inpEMail1, inpPass1, inpName1)

        inpLogin, inpEMail2, inpPass2, inpName2 = xtest_common.createNewUser(self, conf, inpLogin, inpEMail2, inpPass2, inpName2, ["do_not_validate"])

        self.assertBodyTextNotPresent(u"Пользователь '" + inpLogin + u"' успешно создан")

        xtest_common.performLogout(self)

        print "logging as created first user. "
        if not xtest_common.performLogin(self, inpLogin, inpPass1):
            raise selenium_test.TestError("Cannot login as newly created user. ")

        # logout self
        self.gotoUrlByLinkText(u"Выход")

        print "try logging as created second user. "
        if xtest_common.performLogin(self, inpLogin, inpPass2):
            raise selenium_test.TestError("I am able to login as 'second' user with duplicate login and new password. ")



