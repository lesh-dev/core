#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import user


class XcmsAuthSetDuplicateEmailByAdmin(xtest_common.XcmsTest):
    """
    This test checks following functional:
    Add new user and sets him email which is already taken by another user.
    steps:
    create some user A
    create another user B
    set user B's email to email of user A.

    """

    def run(self):
        self.ensure_logged_off()

        # step one: create first user
        inp_login1 = "dup_mail1"
        inp_name1 = u"Вася Тестов"

        u1 = user.User(self)
        u1.create_new_user(
            login=inp_login1,
            name=inp_name1,
            random=True,
            logout_admin=False,
        )

        # step 2: create another user
        inp_login2 = "dup_mail2"
        inp_name2 = u"Миша Тестов"

        # create second user without re-login Admin
        u2 = user.User(self)
        u2.create_new_user(
            login=inp_login2,
            name=inp_name2,
            random=True,
            login_as_admin=False,
        )

        print "logging as created first user. "
        if not self.performLogin(u1.login, u1.password):
            self.failTest("Cannot login as newly created user One. ")

        self.performLogoutFromSite()

        print "logging as created second user. "
        if not self.performLogin(u2.login, u2.password):
            self.failTest("Cannot login as newly created user Two. ")

        self.performLogoutFromSite()

        # login as admin, enter user profile and change some fields.

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "enter user profile in admin CP"

        self.gotoUrlByPartialLinkText(u2.login)

        self.assertElementValueById("name-input", u2.name)
        self.assertElementValueById("email-input", u2.email)

        # try to hack email
        inp_email2_new = u1.email

        inp_email2_new = self.fillElementById("email-input", inp_email2_new)
        print "new email 2: ", inp_email2_new

        self.clickElementById("update_user-submit")

        self.assertBodyTextPresent(u"уже существует")

        # self.performLogoutFromAdminPanel()
