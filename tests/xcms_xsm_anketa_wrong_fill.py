#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import bawlib


class XcmsXsmAnketaWrongFill(xtest_common.XcmsTest):
    """
    This test checks bad cases of anketa add functional
    It does following:
    * navigate to anketa form
    * fill anketa with incorrect values
    * try to submit form
    * correct some values and try submit again
    * correct all errors and finally submit form.
    """

    def trySubmit(self, reason=None):
        self.clickElementById("submit_anketa-submit")
        if reason:
            self.assertBodyTextNotPresent(self.getAnketaSuccessSubmitMessage(), reason)

    def run(self):
        # anketa fill negative test:
        self.gotoRoot()

        # navigate to anketas

        self.gotoUrlByLinkText(self.getEntranceLinkName())
        self.gotoAnketa()

        self.assertBodyTextPresent(self.getAnketaPageHeader())

        # try to submit empty form.
        self.trySubmit("Empty form should not be submitted. ")

        lastNameTooShort = u"Поле 'Фамилия' слишком короткое"

        self.assertBodyTextPresent(lastNameTooShort)

        # generate some text
        inpLastName = u"Криворучкин" + random_crap.random_text(5)
        inpFirstName = u"Хакер" + random_crap.random_text(3)
        inpMidName = u"Ламерович" + random_crap.random_text(3)

        inpBirthDate = random_crap.randomDigits(2) + "." + random_crap.randomDigits(2) + "." + random_crap.randomDigits(4)

        inpSchool = u"Хакерская школа им. К.Митника №" + random_crap.randomDigits(4)

        inpSchoolCity = u"Школа находится в /dev/brain/" + random_crap.random_text(5)
        inpClass = random_crap.randomDigits(1) + u"Х"

        inpPhone = "+7" + random_crap.randomDigits(9)
        inpCell = "+7" + random_crap.randomDigits(9)
        inpEmail = random_crap.random_text(10) + "@" + random_crap.random_text(6) + ".com"
        inpSkype = random_crap.random_text(12)
        inpSocial = random_crap.randomVkontakte()
        inpSocialShow = bawlib.cutHttp(inpSocial)

        inpFav = random_crap.randomCrap(20, ["multiline"])
        inpAch = random_crap.randomCrap(15, ["multiline"])
        inpHob = random_crap.randomCrap(10, ["multiline"])

        # try fill only surname
        inpLastName = self.fillElementById("last_name-input", inpLastName)

        self.trySubmit("Only Last name was filled. ")
        self.assertBodyTextPresent(u"Поле 'Имя' слишком короткое")

        inpFirstName = self.fillElementById("first_name-input", inpFirstName)

        self.trySubmit("Only Last name and First name was filled. ")
        self.assertBodyTextPresent(u"Поле 'Отчество' слишком короткое")

        inpMidName = self.fillElementById("patronymic-input", inpMidName)

        self.trySubmit("Only FIO values were filled. ")
        self.assertBodyTextPresent(u"Класс не указан")

        inpBirthDate = self.fillElementById("birth_date-input", inpBirthDate)
        inpSchool = self.fillElementById("school-input", inpSchool)
        inpSchoolCity = self.fillElementById("school_city-input", inpSchoolCity)

        inpClass = self.fillElementById("current_class-input", inpClass)

        self.trySubmit("Phone fields were not filled. ")
        self.assertBodyTextPresent(u"Укажите правильно хотя бы один из телефонов")

        inpPhone = self.fillElementById("phone-input", inpPhone)
        inpCell = self.fillElementById("cellular-input", inpCell)

        inpEmail = self.fillElementById("email-input", inpEmail)
        inpSkype = self.fillElementById("skype-input", inpSkype)
        inpSocial = self.fillElementById("social_profile-input", inpSocial)

        self.trySubmit("Invalid control question answer. ")
        self.assertBodyTextPresent(u"Неправильный ответ на контрольный вопрос")

        # control question
        self.fillElementById("control_question-input", u"ампер")

        areYouSure = u"Если Вы уверены, что не хотите указывать эту информацию"

        self.trySubmit("Favourites were not filled")
        self.assertBodyTextPresent(areYouSure)

        inpFav = self.fillElementById("favourites-text", inpFav)
        self.trySubmit("Achievements were not filled")
        self.assertBodyTextPresent(areYouSure)

        inpAch = self.fillElementById("achievements-text", inpAch)
        self.trySubmit("Hobbies were not filled")
        self.assertBodyTextPresent(areYouSure)

        inpHob = self.fillElementById("hobby-text", inpHob)

        # and now try to erase one of very important  fields.
        self.fillElementById("last_name-input", "")

        self.trySubmit("Empty last name is not allowed. ")
        self.assertBodyTextPresent(lastNameTooShort)

        # fill it again.
        inpLastName = self.fillElementById("last_name-input", inpLastName)

        self.fillElementById("hobby-text", "")

        self.trySubmit("Hobbies were erased")
        self.assertBodyTextPresent(areYouSure)

        # no erase achievements.
        self.fillElementById("achievements-text", "")
        self.trySubmit("Enter confirmation mode with erased field 'A' and remove another field 'B'. Revalidation check after bug #529")

        inpHob = self.fillElementById("hobby-text", inpHob)
        inpAch = self.fillElementById("achievements-text", inpAch)

        # at last, it should work.
        self.trySubmit()

        # now login as manager
        self.performLoginAsManager()

        self.gotoRoot()

        self.gotoUrlByLinkText(self.getAnketaListMenuName())

        shortAlias = inpLastName + " " + inpFirstName
        fullAlias = shortAlias + " " + inpMidName

        anketaUrlName = shortAlias.strip()
        # try to drill-down into table with new anketa.

        self.gotoUrlByLinkText(anketaUrlName)

        # just check text is on the page.
        self.logAdd("Checking that all filled fields are displayed on the page. ")

        self.checkPersonAliasInPersonView(fullAlias)

        self.assertBodyTextPresent(inpBirthDate)
        self.assertBodyTextPresent(inpSchool)
        self.assertBodyTextPresent(inpSchoolCity)
        self.assertBodyTextPresent(inpClass)
        self.assertBodyTextPresent(inpPhone)
        self.assertBodyTextPresent(inpCell)
        self.assertBodyTextPresent(inpEmail)
        self.assertBodyTextPresent(inpSkype)
        self.assertBodyTextPresent(inpSocialShow)
        self.clickElementById("show-extra-person-info")
        self.wait(1)
        self.assertElementSubTextById("extra-person-info", inpFav)
        self.assertElementSubTextById("extra-person-info", inpAch)
        self.assertElementSubTextById("extra-person-info", inpHob)
