#!/usr/bin/python
# -*- coding: utf8 -*-


import xtest_common


class XcmsPasswordChecker(xtest_common.XcmsTest):

    def run(self):
        url_list = ["http://fizlesh.ru", "http://lesh.org.ru"]
        password_list = ["admin", "password", "root", "pass"]
        login_list = ["admin", "user", "login", "root"]
        for url in url_list:
            self.base_url = url
            for password in password_list:
                for login in login_list:
                    if self.performLogin(login, password):
                        self.failTest("It is possible to login with: {0}, {1}".format(login, password))
