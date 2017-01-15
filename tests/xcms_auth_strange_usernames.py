#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import xtest_common
import random_crap
import user


class XcmsAuthStrangeUsernames(xtest_common.XcmsTest):
    """
    #905

    *positive cases
    <whatever>.user.<whatever>
    <whatever>.user
    user.<whatever>

    *negative cases
    .<whatever>
    @<whatever>
    ../usr/login

    """

    def run(self):

        self.ensure_logged_off()

        #positive cases

        inp_login = "an_test_user_" + ".user."
        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            random=True,
        )
        logging.info("Created a new user: " + u.name)

        inp_login = random_crap.random_text(8) + ".user"
        inp_email = random_crap.randomEmail()
        inp_name = random_crap.random_text(8)
        inp_pass = random_crap.random_text(8)
        u.create_new_user(
            login=inp_login,
            email=inp_email,
            password=inp_pass,
            name=inp_name,
            random=False,
        )
        logging.info("Created a new user: " + u.name)

        inp_login = "user."
        u.create_new_user(
            login=inp_login,
            random=True,
        )
        logging.info("Created a new user: " + u.name)

        #negative cases

        logging.info("Reached negative cases")

        inp_login = ".user"
        u.create_new_user(
            login=inp_login,
            random=True,
            validate=False,
        )
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: " + u.name)
        self.performLogout()

        inp_login = "@user"
        u.create_new_user(
            login=inp_login,
            random=True,
            validate=False,
        )
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: " + u.name)
        self.performLogout()

        inp_login = "../usr/login"
        inp_email = random_crap.randomEmail()
        inp_name = random_crap.random_text(8)
        inp_pass = random_crap.random_text(8)
        u.create_new_user(
            login=inp_login,
            email=inp_email,
            password=inp_pass,
            name=inp_name,
            random=False,
            validate=False,
        )
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: " + u.name)
        self.performLogout()
