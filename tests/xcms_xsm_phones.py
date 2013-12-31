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
        inpPhone = "+7(900)000-00-00, +7(900)999-99-99"

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpPhone = self.fillElementById("cellular-input", inpPhone)
        
        inpPhone = inpPhone.replace("+7", "8")
        
        self.clickElementById("update-person-submit")
        
        self.gotoBackToPersonView()

        fullAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        # check if person alias is present (person saved correctly)
        
        self.checkPersonAliasInPersonView(fullAlias)
        self.assertBodyTextPresent(inpPhone)
        

