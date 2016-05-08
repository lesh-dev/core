#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsXsmPhones(xtest_common.XcmsTest):
    """
    This test checks person phone parsing feature
    It does following:
    * adds new person
    * fill some examples of valid phone specifications
    * checks if they are correctly displayed on person card.
    * checks phone autoformat
    """

    def phoneFix(self, phone):
        return phone.replace("+7", "8").replace("8-900-", "8(900)")

    def run(self):
        self.performLoginAsManager()

        self.gotoXsm()
        self.gotoXsmActive()
        self.gotoXsmAddPerson()

        # generate
        inpLastName = u"Телефонов_" + random_crap.randomText(4)
        inpFirstName = u"Самсунг_" + random_crap.randomText(3)
        inpMidName = u"Нокиевич_" + random_crap.randomText(3)
        inpCellPhones = ["+7(900)000-00-00", "+7(900)999-99-99"]
        inpCellPhoneLine = ", ".join(inpCellPhones)
        inpPhones = ["8-900-000-00-00", "+7-900-999-99-99"]
        inpPhoneLine = ", ".join(inpPhones)

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpCellPhoneLine = self.fillElementById("cellular-input", inpCellPhoneLine)
        inpPhoneLine = self.fillElementById("phone-input", inpPhoneLine)

        inpCellPhones = list(map(self.phoneFix, inpCellPhones))
        inpPhones = list(map(self.phoneFix, inpPhones))

        self.clickElementById("update-person-submit-top")

        self.gotoBackToPersonView()

        fullAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        # check if person alias is present (person saved correctly)

        self.checkPersonAliasInPersonView(fullAlias)

        personId = self.getCurrentPersonId()

        for i in range(0, 2):
            personCellPhoneEleId = "person{0}-cellular-{1}".format(personId, i)
            personPhoneEleId = "person{0}-phone-{1}".format(personId, i)

            siteCellPhone = self.getElementTextById(personCellPhoneEleId)
            sitePhone = self.getElementTextById(personPhoneEleId)
            self.logAdd("Cell phone #{0} on the site: ".format(i) + siteCellPhone)
            self.logAdd("Phone #{0} on the site: ".format(i) + sitePhone)

            if inpCellPhones[i] != siteCellPhone:
                self.failTest("Cell phone #{0} on the site '{1}' don't match entered '{2}'. ".format(i, siteCellPhone, inpCellPhones[i]))
            if inpPhones[i] != sitePhone:
                self.failTest("Phone #{0} on the site '{1}' don't match entered '{2}'. ".format(i, sitePhone, inpPhones[i]))

        self.gotoEditPerson()
        inpPhone = "+79261112233"
        inpPhone = self.fillElementById("phone-input", inpPhone)
        inpCellPhone = "89261112233"
        inpCellPhone = self.fillElementById("cellular-input", inpCellPhone)
        self.clickElementById("update-person-submit-top")
        self.gotoBackToPersonView()

        personCellPhoneEleId = "person{0}-cellular-{1}".format(personId, 0)
        personPhoneEleId = "person{0}-phone-{1}".format(personId, 0)

        siteCellPhone = self.getElementTextById(personCellPhoneEleId)
        sitePhone = self.getElementTextById(personPhoneEleId)

        if sitePhone != "8(926)111-22-33":
            self.failTest("Phone was not autoformatted. ")
        if siteCellPhone != "8(926)111-22-33":
            self.failTest("Cell phone was not autoformatted. ")
