#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
# import bawlib


class XcmsXsmAnketaEdit(xtest_common.XcmsTest):
    """
    This test checks anketa edit functional and following person processing steps.
    Steps:
    * navigate to anketa form
    * fill anketa with correct values
    * submit form
    * login as admin (root)
    * naviagate to anketa list
    * clicks on new anketa
    * checks if entered data match screen form.
    * edits anketa and check that status is left intact
    """

    # -------------------- begining of the test
    def run(self):
        # anketa fill/edit positive test:
        # fields are filled with correct values.

        self.gotoRoot()

        # navigate to anketas

        self.gotoUrlByLinkText(self.getEntranceLinkName())
        self.gotoAnketa()
        self.assertBodyTextPresent(self.getAnketaPageHeader())

        # generate
        inpLastName = u"Анкеткин" + random_crap.randomText(4)
        inpFirstName = u"Юрий" + random_crap.randomText(3)
        inpMidName = u"Петрович" + random_crap.randomText(3)

        inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4)

        inpSchool = u"Какая-то школа №" + random_crap.randomDigits(4)

        inpSchoolCity = u"Магадан-" + random_crap.randomText(5)
        inpClass = random_crap.randomDigits(1) + u" В"

        inpPhone = "+7" + random_crap.randomDigits(9)
        inpCell = "+7" + random_crap.randomDigits(9)
        inpEmail = random_crap.randomText(7) + "@" + random_crap.randomText(6) + ".ru"

        # inpFav = random_crap.randomCrap(8, ["multiline"])
        # inpAch = random_crap.randomCrap(6, ["multiline"])
        # inpHob = random_crap.randomCrap(4, ["multiline"])
        # inpSource = random_crap.randomCrap(5, ["multiline"])

        inpLastName = self.fillElementById("last_name-input", inpLastName)

        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        inpBirthDate = self.fillElementById("birth_date-input", inpBirthDate)
        inpSchool = self.fillElementById("school-input", inpSchool)
        inpSchoolCity = self.fillElementById("school_city-input", inpSchoolCity)
        inpClass = self.fillElementById("current_class-input", inpClass)
        inpPhone = self.fillElementById("phone-input", inpPhone)
        inpCell = self.fillElementById("cellular-input", inpCell)
        inpEmail = self.fillElementById("email-input", inpEmail)
        self.fillElementById("control_question-input", u"ампер")

        self.clickElementById("submit-anketa-button")
        self.assertBodyTextPresent(u"ещё раз")
        self.clickElementById("submit-anketa-button")

        self.assertBodyTextPresent(self.getAnketaSuccessSubmitMessage())

        # now login as admin

        self.performLoginAsManager()

        self.gotoRoot()

        self.gotoUrlByLinkText(self.getAnketaListMenuName())

        shortAlias = xtest_common.shortAlias(inpLastName, inpFirstName)
        fullAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        # print "Full student alias:", fullAlias.encode("utf-8")
        anketaUrlName = shortAlias.strip()
        # try to drill-down into table with new anketa.

        self.gotoUrlByLinkText(anketaUrlName)

        # just check text is on the page.
        print "Checking that filled fields are displayed on the page. "

        self.checkPersonAliasInPersonView(fullAlias)

        self.assertBodyTextPresent(inpBirthDate)
        self.assertBodyTextPresent(inpSchool)
        self.assertBodyTextPresent(inpSchoolCity)
        self.assertBodyTextPresent(inpClass)
        self.assertBodyTextPresent(inpPhone)
        self.assertBodyTextPresent(inpCell)
        self.assertBodyTextPresent(inpEmail)

        # now, let's edit anketa.

        self.gotoEditPerson()

        # TODO: continue

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

        self.assertElementValueById("anketa_status-selector", "new")
        # change anketa field and save it.

        inpSkype = random_crap.randomText(8)
        inpSkype = self.fillElementById("skype-input", inpSkype)

        self.clickElementById("update-person-submit-top")

        self.assertBodyTextPresent(u"Участник успешно сохранён")
        self.gotoBackToAnketaView()

        # check bug
        self.assertElementTextById("anketa_status-span", u"Новый")

        self.gotoRoot()
        self.gotoXsm()
        self.gotoUrlByLinkText(self.getAnketaListMenuName())

        # try to drill-down again into table with new anketa.
        # it should be displayed in this list, not in school participants.
        self.gotoUrlByLinkText(anketaUrlName)
