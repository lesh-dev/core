#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsXsmAvatar(SeleniumTest):
    """
    This test checks person user functional and VK's avatar display feature
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * check person's avatar.
    """

    def run(self):
        self.setAutoPhpErrorChecking(False) #TODO: fix this
        xtest_common.assertNoInstallerPage(self)

        conf = XcmsTestConfig()

        testMailPrefix = conf.getAnketaNamePrefix()

        adminLogin = conf.getAdminLogin()
        adminPass = conf.getAdminPass()

        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), adminLogin, adminPass)
        xtest_common.performLoginAsAdmin(self, adminLogin, adminPass)

        xtest_common.gotoAllPeople(self)

        self.gotoUrlByLinkText(u"Добавить участника")

        # generate
        inpLastName = testMailPrefix + u"Аватаров" + random_crap.randomText(5);
        inpFirstName = u"Петр_" + random_crap.randomText(3)
        inpMidName = u"Палыч_" + random_crap.randomText(3)
        inpSocial = "http://vk.com/vdm_p"

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementByName("update-person")
        
        xtest_common.gotoBackToPersonView(self)

        fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
        # check if person alias is present (person saved correctly)
        self.assertBodyTextPresent(fullAlias)
        # check avatar
        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);
        
        # ok, now let's test xyz100 avatar.
        xtest_common.gotoEditPerson(self)
        
        inpSocial = "http://vk.com/vasya10"
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementByName("update-person")
        xtest_common.gotoBackToPersonView(self)

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);
            
        # ok, now let's test id123456 avatar.
        xtest_common.gotoEditPerson(self)
        
        inpSocial = "http://vk.com/id777314"
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementByName("update-person")
        xtest_common.gotoBackToPersonView(self)

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);

