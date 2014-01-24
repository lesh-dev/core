#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsAuthChangeUserByAdmin(xtest_common.XcmsTest):
    """
    This test checks following functional:
    Add new user and change it's profile by admin (root).
    Then see if proper menu items appear after user login.
    """

    def run(self):
        # first, login as admin
        inpLogin = "priv_user_" + random_crap.randomText(8)
        inpEMail = random_crap.randomEmail()
        inpPass = random_crap.randomText(10)
        inpName = u"Саша Тестов" + random_crap.randomText(6)

        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)

        print "logging as created user. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login as newly created user. ")


        self.assertUrlNotPresent(self.getAdminPanelLinkName(), "default created user should have no Admin rights. ")
        self.assertUrlNotPresent(self.getEditPageInPlaceLinkName(), "default created user should have no Editor rights. ")
        self.assertUrlNotPresent(self.getAnketaListMenuName(), "default created user should have no Manager rights. ")
        print "Okay, no we see that default user is not Admin and not Editor. "

        # logout self
        self.performLogoutFromSite()

        # login as admin, enter user profile and change some fields.

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "enter user profile in admin CP"

        self.gotoUrlByPartialLinkText(inpLogin)

        self.assertElementValueById("name-input", inpName)
        self.assertElementValueById("email-input", inpEMail)

        inpName = inpName + "_changed"

        inpName = self.fillElementById("name-input", inpName)
        print "New user name: ", inpName

        print "Check if administrator priviledge is off now"
        self.assertCheckboxValueById("group_admin-checkbox", False)

        print "Add administrator priviledge"
        self.clickElementById("group_admin-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", True)

        self.clickElementById("update_user")

        self.performLogoutFromAdminPanel()

        print "logging as new user with changed permissions. now he is Admin. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login again as newly created user (with admin privs). ")

        self.assertUrlPresent(self.getAdminPanelLinkName(), "Now user should have Admin priviledges. ")
        self.performLogoutFromSite()

        # ---------------------- 2nd stage: Editor

        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "goto user profile in admin CP"

        self.gotoUrlByPartialLinkText(inpLogin)

        self.assertCheckboxValueById("group_admin-checkbox", True)
        self.assertCheckboxValueById("group_editor-checkbox", False)

        print "Now change priviledges."

        self.clickElementById("group_admin-checkbox")
        self.clickElementById("group_editor-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", True)

        self.clickElementById("update_user")

        self.performLogoutFromAdminPanel()

        print "logging as new user with 2-nd time changed permissions. now he is Editor. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login again as newly created user (with Editor privs). ")

        self.assertUrlPresent(self.getAdminPanelLinkName(), "Now our user should have no Admin rights, but Editor uses admin panel. ")
        self.assertUrlNotPresent(self.getAnketaListMenuName(), "Our user still have no Manager rights. ")
        self.assertUrlPresent(self.getEditPageInPlaceLinkName(), "Now our user should have Editor rights. ")

        self.gotoAdminPanel()
        self.assertUrlNotPresent(self.getUserListLinkName(), "Editor should not see 'Users' menu. ")

        accessDeniedMsg = u"Доступ запрещён"

        self.gotoPage("/?&mode=user_manage&page=index&ref=ladmin")
        self.assertBodyTextPresent(accessDeniedMsg, "Hack of 'users' hidden link succeeded. ")

        self.assertUrlNotPresent(u"Группы", "Editor should not see 'Groups' menu. ")
        self.gotoPage("/?&mode=group_admin&page=index&ref=ladmin")
        self.assertBodyTextPresent(accessDeniedMsg, "Hack of 'groups' hidden link succeeded. ")

        self.performLogoutFromAdminPanel()

        # -------------------------------------- 3 stage: anketa manager
        self.performLoginAsAdmin()

        self.gotoAdminPanel()
        self.gotoUserList()

        print "goto user profile in admin CP"

        self.gotoUrlByPartialLinkText(inpLogin)

        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", True)
        self.assertCheckboxValueById("group_ank-checkbox", False)

        print "Now change priviledges."

        self.clickElementById("group_ank-checkbox")
        self.clickElementById("group_editor-checkbox")
        self.assertCheckboxValueById("group_admin-checkbox", False)
        self.assertCheckboxValueById("group_editor-checkbox", False)
        self.assertCheckboxValueById("group_ank-checkbox", True)

        self.clickElementById("update_user")

        self.performLogoutFromAdminPanel()

        print "logging as new user with 3-rd time changed permissions. now he is Manager. "
        if not self.performLogin(inpLogin, inpPass):
            self.failTest("Cannot login again as newly created user (with Manager privs). ")

        self.assertUrlNotPresent(self.getAdminPanelLinkName(), "Now our user should have no access to Admin panel. ")
        self.assertUrlPresent(self.getAnketaListMenuName(), "Our user should now obtain Manager rights. ")
        self.assertUrlNotPresent(self.getEditPageInPlaceLinkName(), "On third stage, our user should have no Editor rights. ")
        self.performLogoutFromSite()

