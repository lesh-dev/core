#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsXsmAnketaDuplicate(xtest_common.XcmsTest):
    """
    This test checks duplicate anketa add functional
    """

    def generateData(self):
        self.inpLastName = u"Дубликатов" + random_crap.randomText(4)
        self.inpFirstName = u"Петр" + random_crap.randomText(3)
        self.inpMidName = u"Сергеевич" + random_crap.randomText(2)

        self.inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4)

        self.inpSchool = u"Школа дубликатов №" + random_crap.randomDigits(4)

        self.inpSchoolCity = u"Тьмутуроканск-" + random_crap.randomDigits(2)
        self.inpClass = random_crap.randomDigits(1) + u" Дэ"

        self.inpPhone = "+7" + random_crap.randomDigits(9)
        self.inpCell = "+7" + random_crap.randomDigits(9)
        self.inpEmail = random_crap.randomText(8) + "@" + random_crap.randomText(6) + ".ru"
        self.inpSkype = random_crap.randomText(10)
        self.inpSocial = random_crap.randomVkontakte()

        self.inpFav = random_crap.randomCrap(4, ["multiline"])
        self.inpAch = random_crap.randomCrap(5, ["multiline"])
        self.inpHob = random_crap.randomCrap(3, ["multiline"])
        self.inpSource = random_crap.randomCrap(3, ["multiline"])

    def addAnketa(self):
        self.gotoRoot()

        # navigate to anketas

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
        self.fillElementById("control_question-input", u"ампер")

        self.clickElementById("submit_anketa-submit")

    def checkUniqueAnketa(self):

        # now login as admin
        self.personAlias = xtest_common.shortAlias(self.inpLastNameReal, self.inpFirstNameReal)
        # self.personAlias = xtest_common.fullAlias(self.inpLastNameReal, self.inpFirstNameReal, self.inpMidNameReal)

        self.performLoginAsManager()
        self.gotoRoot()
        self.gotoUrlByLinkText(self.getAnketaListMenuName())

        self.fillElementById("show_name_filter-input", self.personAlias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(self.personAlias) != 1:
            self.failTest("Found more than one anketa with exact FIO. Duplicate filtering is broken. ")

    def changeStatus(self):
        self.gotoXsm()
        self.gotoXsmAnketas()
        self.gotoUrlByLinkText(self.personAlias)
        self.gotoXsmChangePersonStatus()

        self.setOptionValueByIdAndValue("anketa_status-selector", "nextyear")
        commentText = u"Меняем статус первой анкете: " + random_crap.randomCrap(5)
        commentText = self.fillElementById("comment_text-text", commentText)

        self.clickElementById("update-person_comment-submit-top")
        self.gotoBackToPersonView()

        self.newState = u"Отложен"
        self.assertBodyTextPresent(u"Статус Новый изменён на {0}".format(self.newState))
        self.assertBodyTextPresent(commentText)

    def checkStatus(self):
        self.gotoXsm()
        self.gotoXsmAnketas()
        self.gotoUrlByLinkText(self.personAlias)
        # anketa should change status to new (like 'ticket reopen')
        self.assertElementTextById("anketa_status-span", u"Новый")

    # -------------------- begining of the test
    def run(self):
        self.ensure_logged_off()

        # add anketa one
        self.generateData()
        self.addAnketa()
        self.assertBodyTextPresent(self.getAnketaSuccessSubmitMessage())
        self.addAnketa()
        self.assertBodyTextNotPresent(self.getAnketaSuccessSubmitMessage())
        self.assertBodyTextPresent(self.getAnketaDuplicateSubmitMessage())

        self.checkUniqueAnketa()

        self.changeStatus()

        self.addAnketa()
        self.assertBodyTextNotPresent(self.getAnketaSuccessSubmitMessage())
        self.assertBodyTextPresent(self.getAnketaDuplicateSubmitMessage())

        self.checkStatus()
