#!/usr/bin/python
# -*- coding: utf8 -*-
import random_crap as rc
import logging


class User(object):

    xtest = None
    login = None
    email = None
    password = None
    name = None

    def __init__(self, xtest):
        self.xtest = xtest
        """self.login = None
        self.email = None
        self.password = None
        self.name = None"""

    def create_new_user(
        self,
        login=str(),
        email=str(),
        password=str(),
        name=str(),
        random=False,
        validate=True,
        manager_rights=False,
        login_as_admin=True,
        logout_admin=True,
    ):
        if random:
            login += "_" + rc.random_text(6)
            email += "_" + rc.randomEmail()
            password += "_" + rc.random_text(6)
            name += "_" + rc.random_text(6)

        logging.info(
            "createNewUser(login: '%s', email: '%s', password: '%s', name: '%s')", login, email, password, name
        )

        if login_as_admin:
            self.xtest.perform_login_as_admin()
            self.xtest.gotoAdminPanel()

        self.xtest.gotoUserList()

        self.xtest.gotoUrlByLinkText(["Create user", u"Создать пользователя"])

        inp_login = self.xtest.fillElementById("login-input", login)
        logging.info("login = '" + inp_login + "'")
        if inp_login == "":
            raise RuntimeError("Filled login value is empty!")

        inpEMail = self.xtest.fillElementById("email-input", email)
        inpPass1 = self.xtest.fillElementById("password-input", password)
        logging.info("original pass: '{0}'".format(password))
        inpPass2 = self.xtest.fillElementById("password_confirm-input", password)
        if inpPass1 != inpPass2:
            raise RuntimeError("Unpredicted input behavior on password entering")
        inpPass = inpPass1
        logging.info("actual pass: '" + inpPass + "'")

        inpName = self.xtest.fillElementById("name-input", name)

        # set notify checkbox.
        # self.clickElementById("notify_user-checkbox")
        # send form

        if manager_rights:
            logging.info("Setting manager rights for user. ")
            # set manager access level
            self.xtest.clickElementById("group_ank-checkbox")

        self.xtest.clickElementByName("create_user")

        self.login = inp_login
        self.email = inpEMail
        self.name = inpName
        self.password = inpPass

        if not validate:
            logging.info("not validating created user, just click create button and shut up. ")
            return inp_login, inpEMail, inpPass, inpName

        logging.info("user created, going to user list again to refresh. ")

        self.xtest.assertBodyTextPresent(u"Пользователь '" + inp_login + u"' успешно создан")

        # refresh user list (re-navigate to user list)
        self.xtest.gotoUserList()

        # enter user profile
        logging.info("entering user profile. ")

        profileLink = inp_login
        # TODO, SITE BUG: make two separate links
        self.xtest.gotoUrlByPartialLinkText(profileLink)

        self.xtest.assertBodyTextPresent(u"Учётные данные")
        self.xtest.assertBodyTextPresent(u"Привилегии")

        # temporary check method
        # test user login
        self.xtest.assertTextPresent("//div[@class='user-ops']", inp_login)
        # test user creator (root)
        self.xtest.assertTextPresent("//div[@class='user-ops']", self.xtest.m_conf.get_admin_login())
        self.xtest.assertElementValueById("name-input", inpName)
        self.xtest.assertElementValueById("email-input", inpEMail)

        # logoff root
        if logout_admin:
            self.xtest.performLogout()

        return inp_login, inpEMail, inpPass, inpName
