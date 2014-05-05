#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsXsmAddSchool(xtest_common.XcmsTest):
    """
    This test checks school add functional.
    * login as manager
    * enter XSM
    * add new school
    * check school list
    * check school in panel
    * edit school properties and save
    """

    def run(self):

        self.performLoginAsManager()
        self.gotoXsm()
        self.gotoXsmSchools()
        self.gotoUrlByLinkText(u"Добавить школу")

        # generate school number
        lastDigit = random_crap.randomDigits(1)

        inpSchoolTitle = u"ЛЭШ_202" + lastDigit + "_" + random_crap.randomWord(6);
        inpStart = "202" + lastDigit + ".07.15"
        inpEnd = "202" + lastDigit + ".08.16"
        inpLocation = u"Деревня Гадюкино_" + random_crap.randomWord(6)

        inpSchoolTitle = self.fillElementByName("school_title", inpSchoolTitle)
        inpStart = self.fillElementByName("school_date_start", inpStart)
        inpEnd = self.fillElementByName("school_date_end", inpEnd)
        inpLocation = self.fillElementByName("school_location", inpLocation)

        self.clickElementByName("update-school")
        self.gotoBackToSchoolView()

        self.assertBodyTextPresent(inpSchoolTitle)
        self.assertBodyTextPresent(inpStart)
        self.assertBodyTextPresent(inpEnd)
        self.assertBodyTextPresent(inpLocation)

        self.gotoUrlByLinkText(u"Правка")

        inpStart = "202" + lastDigit + ".07.23"
        inpEnd = "202" + lastDigit + ".08.23"

        inpStart = self.fillElementByName("school_date_start", inpStart)
        inpEnd = self.fillElementByName("school_date_end", inpEnd)
        inpLocation = self.fillElementByName("school_location", inpLocation)

        self.clickElementByName("update-school")

        self.gotoBackToSchoolView()

        self.assertBodyTextPresent(inpSchoolTitle)
        self.assertBodyTextPresent(inpStart)
        self.assertBodyTextPresent(inpEnd)
        self.assertBodyTextPresent(inpLocation)

