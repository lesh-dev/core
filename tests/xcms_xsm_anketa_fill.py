#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsXsmAnketaFill(SeleniumTest):
    """
    This test checks anketa add functional and following person processing steps.
    It does following:
    * navigates to anketa form
    * fill anketa with all correct values
    * submits form
    * login as admin (root)
    * naviagates to anketa list
    * clicks on new anketa
    * checks if all enetered data match screen form.
    * adds 3 comments to this new person
    * edits 2 of 3 comments
    * changes person status incrementally
    * TODO: change personal data
    * TODO: make 'active'
    * TODO: check presence in active list
    * TODO: add person to some schools.
    * TODO: remove person from one of schools
    """
    
    def addCommentsToPerson(self):
        commentText1 = xtest_common.addCommentToPerson(self)
        print "Added first comment: ", commentText1
        self.assertBodyTextPresent(commentText1)

        commentText2 = xtest_common.addCommentToPerson(self)
        print "Added second comment: ", commentText2
        self.assertBodyTextPresent(commentText2)

        commentText3 = xtest_common.addCommentToPerson(self)
        print "Added third comment: ", commentText3
        self.assertBodyTextPresent(commentText3)

        # and now let's edit one of them.

        self.gotoIndexedUrlByLinkText(u"Правка", 0)
        xtest_common.gotoBackAfterComment(self)

        self.gotoIndexedUrlByLinkText(u"Правка", 1)
        xtest_common.gotoBackAfterComment(self)

        # oh, no! we want to use comment link ids!

        commentTextNew1 = xtest_common.editCommentToPerson(self, "comment-edit-1")
        self.assertBodyTextPresent(commentTextNew1)

        commentTextNew3 = xtest_common.editCommentToPerson(self, "comment-edit-3")
        self.assertBodyTextPresent(commentTextNew3)

        # check if all new comments are present here, and 2-nd comment left unchanged

        self.assertBodyTextPresent(commentTextNew1, "Comment 1 must change value. ")
        self.assertBodyTextPresent(commentText2, "Comment should remain unchanged. ")
        self.assertBodyTextPresent(commentTextNew3, "Comment 3 must change value. ")

    # -------------------- begining of the test
    def run(self):
        # anketa fill positive test:
        # all fields are filled with correct values.
        conf = XcmsTestConfig()

        self.setAutoPhpErrorChecking(conf.getPhpErrorCheckFlag())
        xtest_common.assertNoInstallerPage(self)
        
        testMailPrefix = conf.getAnketaNamePrefix()
        
        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), conf.getAdminLogin(), conf.getAdminPass())
            
        self.gotoRoot()
        
        #navigate to anketas
        
        self.gotoUrlByLinkText(u"Поступление")
        self.gotoUrlByLinkText(u"Анкета")
        self.assertBodyTextPresent(u"Регистрационная анкета")
            
        # generate
        inpLastName = testMailPrefix + u"Чапаев" + random_crap.randomText(5);
        inpFirstName = u"Василий" + random_crap.randomText(3)
        inpMidName = u"Иваныч" + random_crap.randomText(3)
        
        inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4);
        
        inpSchool = u"Тестовая школа им. В.Е.Бдрайвера №" + random_crap.randomDigits(4)
        
        inpSchoolCity = u"Школа находится в /var/opt/" + random_crap.randomText(5)
        inpClass = random_crap.randomDigits(1) + u" Гэ"
        
        inpPhone = "+7" + random_crap.randomDigits(9)
        inpCell = "+7" + random_crap.randomDigits(9)
        inpEmail = random_crap.randomText(10) + "@" + random_crap.randomText(6) + ".ru"
        inpSkype = random_crap.randomText(12)
        inpSocial = random_crap.randomVkontakte()
        
        inpFav = random_crap.randomCrap(20, ["multiline"])
        inpAch = random_crap.randomCrap(15, ["multiline"])
        inpHob = random_crap.randomCrap(10, ["multiline"])
        inpSource = random_crap.randomCrap(10, ["multiline"])
        
        inpLastName = self.fillElementById("last_name-input", inpLastName)
        
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpBirthDate = self.fillElementById("birth_date-input", inpBirthDate)
        inpSchool = self.fillElementById("school-input", inpSchool)
        inpSchoolCity = self.fillElementById("school_city-input", inpSchoolCity)
        inpClass = self.fillElementById("current_class-input", inpClass)
        inpPhone = self.fillElementById("phone-input",inpPhone)
        inpCell = self.fillElementById("cellular-input", inpCell)
        inpEmail = self.fillElementById("email-input", inpEmail)
        inpSkype = self.fillElementById("skype-input", inpSkype)
        inpSocial = self.fillElementById("social_profile-input", inpSocial)
        inpFav = self.fillElementById("favourites-text", inpFav)
        inpAch = self.fillElementById("achievements-text", inpAch)
        inpHob = self.fillElementById("hobby-text", inpHob)
        inpSource = self.fillElementById("lesh_ref-text", inpSource)
        
        self.clickElementById("submit-anketa-button")
        
        self.assertBodyTextPresent(u"Спасибо, Ваша анкета принята!")
        
            
    # now login as admin
    
        adminLogin = conf.getAdminLogin()
        adminPass = conf.getAdminPass()
    
        xtest_common.performLoginAsAdmin(self, adminLogin, adminPass)
        
        self.gotoRoot()
            
        self.gotoUrlByLinkText(u"Анкеты")
        
        shortAlias = inpLastName + " " + inpFirstName
        fullAlias = shortAlias + " " + inpMidName
        #print "Full student alias:", fullAlias.encode("utf-8")
        anketaUrlName = shortAlias.strip()
        # try to drill-down into table with new anketa.

        self.gotoUrlByLinkText(anketaUrlName)

    # just check text is on the page.
        print "Checking that all filled fields are displayed on the page. "
        
        self.assertElementTextById("person-title", fullAlias)
        self.assertBodyTextPresent(inpBirthDate)
        self.assertBodyTextPresent(inpSchool)
        self.assertBodyTextPresent(inpSchoolCity)
        self.assertBodyTextPresent(inpClass)
        self.assertBodyTextPresent(inpPhone)
        self.assertBodyTextPresent(inpCell)
        self.assertBodyTextPresent(inpEmail)
        self.assertBodyTextPresent(inpSkype)
        self.assertBodyTextPresent(inpSocial)
        self.clickElementById("show-extra-person-info")
        self.wait(1)
        self.assertElementSubTextById("extra-person-info", inpFav)
        self.assertElementSubTextById("extra-person-info", inpAch)
        self.assertElementSubTextById("extra-person-info", inpHob)
        self.assertElementSubTextById("extra-person-info", inpSource)
        
        self.addCommentsToPerson()
        
        # now, let's change anketa status to "Ждет собеседования"
        
        self.gotoUrlByLinkText(u"Редактировать анкетные данные")
        
        # first, check that values in opened form match entered in anketa.

        self.assertElementValueById("last_name-input", inpLastName)
        self.assertElementValueById("first_name-input", inpFirstName)
        self.assertElementValueById("patronymic-input", inpMidName)
        self.assertElementValueById("birth_date-input", inpBirthDate)
        self.assertElementValueById("school-input", inpSchool)
        self.assertElementValueById("school_city-input", inpSchoolCity)
        self.assertElementValueById("ank_class-input", inpClass)
        # current_class should now be equal to ank_class (fresh anketa)
        self.assertElementValueById("current_class-input", inpClass)
        self.assertElementValueById("phone-input", inpPhone)
        self.assertElementValueById("cellular-input", inpCell)
        self.assertElementValueById("email-input", inpEmail)
        self.assertElementValueById("skype-input", inpSkype)
        self.assertElementValueById("social_profile-input", inpSocial)
        self.assertElementValueById("favourites-text", inpFav)
        self.assertElementValueById("achievements-text", inpAch)
        self.assertElementValueById("hobby-text", inpHob)
        self.assertElementValueById("lesh_ref-text", inpSource)
        
        self.assertElementValueById("anketa_status-selector", "new")
        # change anketa status and save it.
        
        self.setOptionValueById("anketa_status-selector", "progress")
        
        self.clickElementById("update-person-submit")
        
        self.assertBodyTextPresent(u"Участник успешно сохранён")
        xtest_common.gotoBackToAnketaView(self)
        
        self.assertElementTextById("anketa_status-span", u"Ждёт собес.")
