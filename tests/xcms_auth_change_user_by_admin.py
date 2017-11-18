#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import user


class XcmsAuthChangeUserByAdmin(xtest_common.XcmsTest):
    """
    This test checks following functional:
    Add new user and change it's profile by admin (root).
    Then see if proper menu items appear after user login.
    """

    def run(self):
        self.ensure_logged_off()

        # first, login as admin

        inp_login = "priv_user_"
        inp_name = u"Саша Тестов"
        u = user.User(self)
        u.create_new_user(
            login=inp_login,
            name=inp_name,
            random=True,
        )

        print "logging as created user. "
        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login as newly created user. ")

        self.assertUrlNotPresent(self.admin_panel_link_name(), "Default created user should have no Admin rights. ")
        self.assertUrlNotPresent(
            self.getEditPageInPlaceLinkName(), "Default created user should have no Editor rights. "
        )
        self.assertUrlNotPresent(self.getAnketaListMenuName(), "default created user should have no Manager rights. ")
        print "Okay, no we see that default user is not Admin and not Editor. "

        # logout self
        self.performLogoutFromSite()

        # login as admin, enter user profile and change some fields.

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "enter user profile in admin CP"

        self.gotoUrlByPartialLinkText(u.login)

        self.assertElementValueById("name-input", u.name)
        self.assertElementValueById("email-input", u.email)

        u.name += "_changed"

        u.name = self.fillElementById("name-input", u.name)
        print "New user name: ", u.name

        print "Check if administrator priviledge is off now"
        self.assertCheckboxValueById("group_admin-checkbox", False)

        print "Add administrator priviledge"
        self.clickElementById("group_admin-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", True)

        self.clickElementById("update_user-submit")

        self.performLogoutFromAdminPanel()

        print "logging as new user with changed permissions. now he is Admin. "
        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login again as newly created user (with admin privs). ")

        self.getElementById("admin", reason="Now user should have Admin priviledges. ")
        self.performLogoutFromSite()

        # ---------------------- 2nd stage: Editor

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "goto user profile in admin CP"

        self.gotoUrlByPartialLinkText(u.login)

        self.assertCheckboxValueById("group_admin-checkbox", True)
        self.assertCheckboxValueById("group_editor-checkbox", False)

        print "Now change priviledges."

        self.clickElementById("group_admin-checkbox")
        self.clickElementById("group_editor-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", True)

        self.clickElementById("update_user-submit")

        self.performLogoutFromAdminPanel()

        print "logging as new user with 2-nd time changed permissions. now he is Editor. "
        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login again as newly created user (with Editor privs). ")

        self.getElementById("admin", "Now our user should have no Admin rights, but Editor uses admin panel. ")
        self.assertUrlNotPresent(self.getAnketaListMenuName(), "Our user still have no Manager rights. ")
        self.assertUrlPresent(self.getEditPageInPlaceLinkName(), "Now our user should have Editor rights. ")

        self.gotoAdminPanel()
        self.assertUrlNotPresent(self.getUserListLinkName(), "Editor should not see 'Users' menu. ")

        accessDeniedMsg = u"Доступ запрещён"

        self.gotoPage("/?&mode=user_manage&page=index&ref=admin")
        self.assertBodyTextPresent(accessDeniedMsg, "Hack of 'users' hidden link succeeded. ")

        # custom groups removed, so group link checking is obsolete

        self.performLogoutFromAdminPanel()

        # -------------------------------------- 3 stage: anketa manager
        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "goto user profile in admin CP"

        self.gotoUrlByPartialLinkText(u.login)

        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", True)
        self.assertCheckboxValueById("group_ank-checkbox", False)

        print "Now change priviledges."

        self.clickElementById("group_ank-checkbox")
        self.clickElementById("group_editor-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", False)
        self.assertCheckboxValueById("group_ank-checkbox", True)

        self.clickElementById("update_user-submit")

        self.performLogoutFromAdminPanel()

        print "logging as new user with 3-rd time changed permissions. now he is Manager. "
        if not self.performLogin(u.login, u.password):
            self.failTest("Cannot login again as newly created user (with Manager privs). ")

        self.assertUrlNotPresent(self.admin_panel_link_name(), "Now our user should have no access to Admin panel. ")
        self.getElementById("xsm", "Now user should have Manager rights and have XSM access")
        self.assertUrlNotPresent(
            self.getEditPageInPlaceLinkName(), "On third stage, our user should have no Editor rights. "
        )
        self.performLogoutFromSite()
