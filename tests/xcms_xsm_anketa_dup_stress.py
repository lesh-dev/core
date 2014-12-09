#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsXsmAnketaDupStress(xtest_common.XcmsTest):
    """
    This test checks duplicate anketa merging algorithm.
    """
    
    def generateData(self):
        self.inpLastName = u"Спамеров" + random_crap.randomText(4)
        self.inpFirstName = u"Егор" + random_crap.randomText(3)
        self.inpMidName = u"Федорович" + random_crap.randomText(2)
        
        self.inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4);
        
        self.inpSchool = u"Школа спамеров №" + random_crap.randomDigits(4)
        
        self.inpSchoolCity = u"Спамерово-" + random_crap.randomDigits(2)
        self.inpClass = random_crap.randomDigits(1) + u" Жэ"
        
        self.inpPhone = "+7" + random_crap.randomDigits(9)
        self.inpCell = "+7" + random_crap.randomDigits(9)
        self.inpEmail = random_crap.randomText(7) + "@" + random_crap.randomText(5) + ".ru"
        
    def generateAuxData(self, iteration, random=False):
        self.inpSkype = random_crap.randomText(8)
        self.inpSocial = random_crap.randomVkontakte()
              
        fmt = u"iteration {0}_{1}"
        if not random:
            fav = "my_favourites"
            ach = "some_achievements"
            hob = "different_hobbies"
            src = "wtf_source"
        else:
            crapParams = (30, ["multiline"])
            crapFunc = random_crap.randomCrap
            fav = crapFunc(*crapParams)
            ach = crapFunc(*crapParams)
            hob = crapFunc(*crapParams)
            src = crapFunc(*crapParams)
        self.inpFav = fmt.format(iteration, fav)
        self.inpAch = fmt.format(iteration, ach)
        self.inpHob = fmt.format(iteration, hob)
        self.inpSource = fmt.format(iteration, src)

    def addAnketa(self):
        self.gotoRoot()
        #navigate to anketas
        self.gotoUrlByLinkText(self.getEntranceLinkName())
        self.gotoAnketa()
        self.assertBodyTextPresent(self.getAnketaPageHeader())
            
        # generate
        self.inpLastNameReal = self.fillElementById("last_name-input", self.inpLastName)
        self.inpFirstNameReal = self.fillElementById("first_name-input", self.inpFirstName)
        self.inpMidNameReal = self.fillElementById("patronymic-input", self.inpMidName)
        self.inpBirthDateReal = self.fillElementById("birth_date-input", self.inpBirthDate)
        self.inpSchoolReal = self.fillElementById("school-input", self.inpSchool)
        self.inpSchoolCityReal = self.fillElementById("school_city-input", self.inpSchoolCity)
        self.inpClassReal = self.fillElementById("current_class-input", self.inpClass)
        self.inpPhoneReal = self.fillElementById("phone-input", self.inpPhone)
        self.inpEmailReal = self.fillElementById("email-input", self.inpEmail)
        self.inpFavReal = self.fillElementById("favourites-text", self.inpFav)
        self.inpAchReal = self.fillElementById("achievements-text", self.inpAch)
        self.inpHobReal = self.fillElementById("hobby-text", self.inpHob)
        self.inpSourceReal = self.fillElementById("lesh_ref-text", self.inpSource)
        
        self.clickElementById("submit-anketa-button")
    
    def checkUniqueAnketa(self):
            
        # now login as admin
        self.personAlias = xtest_common.shortAlias(self.inpLastNameReal, self.inpFirstNameReal)
        # self.personAlias = xtest_common.fullAlias(self.inpLastNameReal, self.inpFirstNameReal, self.inpMidNameReal)
        
        self.performLoginAsManager()
        self.gotoRoot()
        self.gotoUrlByLinkText(self.getAnketaListMenuName())
        
        alias = self.fillElementById("show_name_filter-input", self.personAlias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(self.personAlias) != 1:
            self.failTest("Found more than one anketa with exact FIO. Duplicate filtering is broken. ")
        self.gotoRoot()
        self.performLogoutFromSite()
                
    # -------------------- begining of the test
    def run(self):
        self.generateData()
        for i in range(0, 5):
            self.generateAuxData(i, random=True)
            self.addAnketa()
            if i == 0:
                self.assertBodyTextPresent(self.getAnketaSuccessSubmitMessage())
            else:
                self.assertBodyTextNotPresent(self.getAnketaSuccessSubmitMessage())
                self.assertBodyTextPresent(self.getAnketaDuplicateSubmitMessage())
        
        self.checkUniqueAnketa()
