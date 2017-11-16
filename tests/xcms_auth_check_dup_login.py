#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import user
import logging


class XcmsAuthCheckDupLogin(xtest_common.XcmsTest):
    """
    add two users with identical logins.
    """

    def run(self):
        self.ensure_logged_off()

        # first, login as admin
        inp_login = "dup_user_" + random_crap.random_text(8)
        inp_email1 = random_crap.randomEmail()
        inp_email2 = random_crap.randomEmail()
        inp_pass1 = random_crap.random_text(10)
        inp_pass2 = random_crap.random_text(10)
        inp_name1 = u"Вася " + random_crap.random_text(6)
        inp_name2 = u"Петя " + random_crap.random_text(6)

        u1 = user.User(self)
        u1.create_new_user(
            login=inp_login,
            email=inp_email1,
            password=inp_pass1,
            name=inp_name1,
            random=False,
        )

        u2 = user.User(self)
        u2.create_new_user(
            login=inp_login,
            email=inp_email2,
            password=inp_pass2,
            name=inp_name2,
            random=False,
            validate=False,
        )

        self.assertBodyTextNotPresent(u"Пользователь '" + inp_login + u"' успешно создан")

        self.performLogout()

        self.logAdd("logging as created first user. ")
        if not self.performLogin(u1.login, u1.password):
            self.failTest("Cannot login as newly created user. ")

        # logout self
        self.performLogout()

        logging.info("try logging as created second user.")
        if self.performLogin(u2.login, u2.password):
            self.failTest("I am able to login as 'second' user with duplicate login and new password. ")
