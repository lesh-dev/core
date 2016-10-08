#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsXsmListFilters(xtest_common.XcmsTest):
    """
    This test checks various filters in XSM lists.
    """

    def testExistingPeople(self):
        # one line expected
        self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        shortAlias = u"Вельтищев Михаил"
        alias = shortAlias + u" Николаевич"

        self.FIOFilterId = "show_name_filter-input"
        self.fillElementById("show_name_filter-input", alias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(shortAlias) != 1:
            self.failTest("Found more than one anketa with exact FIO. Filters are broken. ")

        # two lines expected
        # self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        shortAliases = [u"Вельтищев Михаил", u"Вельтищев Дмитрий"]
        alias = u"Вельтищев"
        self.fillElementById(self.FIOFilterId, alias)

        self.clickElementByName("show-person")

        for alias in shortAliases:
            if self.countIndexedUrlsByLinkText(alias) != 1:
                self.failTest("Expected link {0} not found. Filters are broken. ".format(alias))

        # none lines expected
        # self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        alias = "qwerty"
        alias = self.fillElementById(self.FIOFilterId, alias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(alias) != 0:
            self.failTest("This search should not return anything. Filters are broken. ")

        # 1 line expected
        # self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        alias = u"Демарин Дмитрий"
        self.fillElementById("show_name_filter-input", alias)
        self.sendEnterById(self.FIOFilterId)

        for it in xrange(3):
            # sometimes it returns 0 links. Seems to be webdriver bug.
            if self.countIndexedUrlsByLinkText(alias) != 1:
                self.logAdd("One more time...")
                self.wait(1)
            else:
                break
        else:
            self.failTest("This search should return one record. Filters are broken. ")

    def testDepartmentSelector(self):
        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()

        # generate
        inpLastName = u"Гуглов" + random_crap.randomText(3)
        inpFirstName = u"Индекс_" + random_crap.randomText(3)
        inpMidName = u"Яхович_" + random_crap.randomText(3)

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)

        department_id = 3  # Математическое
        self.setOptionValueByIdAndValue("department_id-selector", department_id)
        # self.setOptionValueByNameAndValue("department_id", department)
        self.clickElementById("update-person-submit")

        self.gotoBackToPersonView()
        self.gotoXsmAllPeople()
        self.setOptionValueByIdAndValue("show_department_id-selector", department_id)

        alias = xtest_common.shortAlias(inpLastName, inpFirstName)
        self.fillElementById(self.FIOFilterId, alias)
        self.clickElementByName("show-person")

        if self.countIndexedUrlsByLinkText(alias) != 1:
            self.failTest("Search with proper department selection return one record. Filters are broken. ")

        self.setOptionValueByIdAndValue("show_department_id-selector", u"Другое")
        self.fillElementById(self.FIOFilterId, alias)
        self.clickElementByName("show-person")

        if self.countIndexedUrlsByLinkText(alias) != 0:
            self.failTest("Search with wrong department should return none records. Filters are broken. ")

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()
        self.gotoRoot()
        self.gotoXsm()
        self.gotoXsmAllPeople()

        self.testExistingPeople()
        self.testDepartmentSelector()
