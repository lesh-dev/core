#!/usr/bin/env python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import user


class XcmsAuthCheckDupEmail(xtest_common.XcmsTest):
    """
    add two users with identical e-mails.
    """

    def run(self):
        self.ensure_logged_off()

        inp_login1 = "dup_email_" + random_crap.random_text(8)
        inp_login2 = "dup_email_" + random_crap.random_text(8)
        inp_email = random_crap.randomEmail()
        inp_pass1 = random_crap.random_text(10)
        inp_pass2 = random_crap.random_text(10)
        inp_name1 = u"Вася " + random_crap.random_text(6)
        inp_name2 = u"Петя " + random_crap.random_text(6)

        u1 = user.User(self)
        u1.create_new_user(
            login=inp_login1,
            email=inp_email,
            password=inp_pass1,
            name=inp_name1,
            random=False,
        )

        u2 = user.User(self)
        u2.create_new_user(
            login=inp_login2,
            email=inp_email,
            password=inp_pass2,
            name=inp_name2,
            random=False,
            validate=False,
        )

        self.assertBodyTextNotPresent(
            u"Пользователь '{}' успешно создан".format(u2.login),
            "We should get error about duplicate e-mails. ",
        )

        self.performLogout()

        print "logging as first created user. "
        if not self.performLogin(u1.login, u1.password):
            self.failTest("Cannot login as newly created first user. ")

        self.performLogout()

        print "try logging as second created user. "
        if self.performLogin(u2.login, u2.password):
            self.failTest("I was able to login as second user with duplicate e-mail. ")
