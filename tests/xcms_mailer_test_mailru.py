#!/usr/bin/python
# -*- coding: utf8 -*-


import xtest_common
import random_crap
import user


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
        self.ensure_logged_off()

        self.gotoRoot()

        inpEMail = self.m_conf.getValidEmail('mail.ru')
        self.removePreviousUsersWithTestEmail(inpEMail)

        # first, login as admin
        inp_login = "an_mailru_user_" + random_crap.random_text(8)
        inp_name = u"Вася Пупкин" + random_crap.random_text(6)

        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            name=inp_name,
            random=True,
        )

        print "logging as created user. "
        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login as newly created user. ")
