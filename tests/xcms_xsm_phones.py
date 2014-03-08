#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsXsmPhones(xtest_common.XcmsTest):
    """
    This test checks person phone parsing feature
    It does following:
    * adds new person
    * fill some examples of valid phone specifications
    * checks if they are correctly displayed on person card.
    """

    def run(self):

        self.performLoginAsManager()

        self.gotoAllPeople()
        self.gotoAddPerson()
        
        # generate
        inpLastName = u"Телефонов_" + random_crap.randomText(4);
        inpFirstName = u"Самсунг_" + random_crap.randomText(3)
        inpMidName = u"Нокиевич_" + random_crap.randomText(3)
        inpCellPhone = "+7(900)000-00-00, +7(900)999-99-99"
        inpPhone = "8-900-000-00-00, +7-900-999-99-99"

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpCellPhone = self.fillElementById("cellular-input", inpCellPhone)
        inpPhone = self.fillElementById("phone-input", inpPhone)
        
        inpCellPhone = inpCellPhone.replace("+7", "8")
        inpPhone = inpPhone.replace("+7", "8")
        
        self.clickElementById("update-person-submit")
        
        self.gotoBackToPersonView()

        fullAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        # check if person alias is present (person saved correctly)
        
        self.checkPersonAliasInPersonView(fullAlias)
        
        personId = self.getCurrentPersonId()
        personCellPhoneEleId = "person" + str(personId) + "-cellular"
        personPhoneEleId = "person" + str(personId) + "-phone"
        
        siteCellPhone = self.getElementTextById(personCellPhoneEleId)
        sitePhone = self.getElementTextById(personPhoneEleId)
        self.logAdd("Cell phone on the site: " + siteCellPhone)
        self.logAdd("Phone on the site: " + sitePhone)
        
        if inpCellPhone != siteCellPhone:
            self.failTest("Cell phones on the site don't match entered cell phones. ")
        if inpPhone != sitePhone:
            self.failTest("Phones on the site don't match entered phones. ")
        

