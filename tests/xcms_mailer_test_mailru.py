#!/usr/bin/python
# -*- coding: utf8 -*-


import xtest_common
import random_crap


class XcmsMailerTestMailRu(xtest_common.XcmsTest):
    """
    This test checks mail.ru via user add functional.
    It does following steps:
    * login as root user
    * navigate to user control panes
    * add random user
    Mail contents checking/readability is up to developer,
    but it is a *MOST* important part of the test.
    """

    def run(self):
        self.gotoRoot()

        # first, login as admin
        inpLogin = "an_mailru_user_" + random_crap.randomText(8)
        inpEMail = self.m_conf.getValidEmail('mail.ru')
        inpPass = random_crap.randomText(10)
        inpName = u"Вася Пупкин" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)

        print "logging as created user. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login as newly created user. ")
