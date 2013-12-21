#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsXsmAvatar(xtest_common.XcmsTest):
    """
    This test checks person user functional and VK's avatar display feature
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * check person's avatar.
    * change avatar to xyz100
    * check person's avatar.
    * change avatar to idNNN
    * check person's avatar.
    * change avatar to default
    * check person's avatar (stalin50).
    * change avatar to non-existing VK page
    * check person's avatar
    """

    def run(self):

        testMailPrefix = self.m_conf.getAnketaNamePrefix()

        self.performLoginAsAdmin()

        self.gotoAllPeople()

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
        
        self.clickElementById("update-person-submit")
        
        self.gotoBackToPersonView()

        fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
        # check if person alias is present (person saved correctly)
        
        self.checkPersonAliasInPersonView(fullAlias)
        # check avatar
        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);
        
        # ok, now let's test xyz100 avatar.
        self.gotoEditPerson()
        
        inpSocial = "http://vk.com/vasya10"
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementById("update-person-submit")
        self.gotoBackToPersonView()

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);
            
        # ok, now let's test id123456 avatar.
        self.gotoEditPerson()
        
        inpSocial = "http://vk.com/id777314"
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementById("update-person-submit")
        self.gotoBackToPersonView()

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" in avatarSrc:
            self.failTest("Wrong (default) avatar detected, expected custom image. VK ID: " + inpSocial);
            
        # ok, now let's test default avatar.
        self.gotoEditPerson()
        
        inpSocial = ""
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementById("update-person-submit")
        self.gotoBackToPersonView()

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" not in avatarSrc:
            self.failTest("Default avatar expected. Current src: " + avatarSrc);

        # ok, now let's test non-existing VK page.
        self.gotoEditPerson()
        
        inpSocial = "http://vk.com/id12345678901234567890"
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        
        self.clickElementById("update-person-submit")
        self.gotoBackToPersonView()

        avatarSrc = self.getImageSrcById("avatar")
        print "Avatar Source: ", avatarSrc
        if "stalin50" not in avatarSrc:
            self.failTest("Default avatar expected. Current src: " + avatarSrc);


