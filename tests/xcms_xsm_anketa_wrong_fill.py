#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

import xsm
import xtest_common
import random_crap
import bawlib


class XcmsXsmAnketaWrongFill(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks bad cases of anketa add functional
    It does following:
    * navigate to anketa form
    * fill anketa with incorrect values
    * try to submit form
    * correct some values and try submit again
    * correct all errors and finally submit form.
    """

    def ensure_not_submitted(self, reason):
        self.assertBodyTextNotPresent(self.get_anketa_success_submit_message(), reason)

    def run(self):
        self.ensure_logged_off()
        self.gotoRoot()

        # navigate to anketas
        self.gotoUrlByLinkText(self.getEntranceLinkName())
        self.goto_anketa()
        self.assertBodyTextPresent(self.getAnketaPageHeader())

        person = xsm.Person(self)
        # try to submit empty form.
        person.input(ank_mode=True)
        self.ensure_not_submitted("Empty form should not be submitted. ")
        last_name_too_short = u"Поле 'Фамилия' слишком короткое"
        self.assertBodyTextPresent(last_name_too_short)

        # generate some text
        person.last_name = u"Криворучкин" + random_crap.random_text(5)
        person.first_name = u"Хакер" + random_crap.random_text(3)
        person.patronymic = u"Ламерович" + random_crap.random_text(3)
        person.birth_date = random_crap.date()
        person.school = u"Хакерская школа им. К.Митника №" + random_crap.randomDigits(4)
        person.school_city = u"Школа находится в /dev/brain/" + random_crap.random_text(5)
        person.ank_class = random_crap.randomDigits(1) + u"Х"
        person.phone = random_crap.phone()
        person.cellular = random_crap.phone()
        person.email = random_crap.email()
        person.skype = random_crap.random_text(12)
        person.social_profile = random_crap.randomVkontakte()
        social_profile_show = bawlib.cut_http(person.social_profile)

        favourites = random_crap.randomCrap(20, ["multiline"])
        achievements = random_crap.randomCrap(15, ["multiline"])
        hobby = random_crap.randomCrap(10, ["multiline"])

        # try fill only surname
        person.input(last_name=person.last_name, ank_mode=True)
        self.ensure_not_submitted("Only Last name was filled. ")
        self.assertBodyTextPresent(u"Поле 'Имя' слишком короткое")

        person.input(first_name=person.first_name, ank_mode=True)
        self.ensure_not_submitted("Only Last name and First name was filled. ")
        self.assertBodyTextPresent(u"Поле 'Отчество' слишком короткое")

        person.input(patronymic=person.patronymic, ank_mode=True)
        self.ensure_not_submitted("Only FIO values were filled. ")
        self.assertBodyTextPresent(u"Класс не указан")

        person.input(
            birth_date=person.birth_date,
            school=person.school,
            school_city=person.school_city,
            ank_class=person.ank_class,
            ank_mode=True,
        )
        self.ensure_not_submitted("Phone fields were not filled. ")
        self.assertBodyTextPresent(u"Укажите правильно хотя бы один из телефонов")

        person.input(
            phone=person.phone,
            cellular=person.cellular,
            email=person.email,
            skype=person.skype,
            social_profile=person.social_profile,
            ank_mode=True,
        )
        self.ensure_not_submitted("Invalid control question answer. ")
        self.assertBodyTextPresent(u"Неправильный ответ на контрольный вопрос")

        person.input(control_question=u"ампер", ank_mode=True)
        self.ensure_not_submitted("Favourites were not filled")
        are_you_sure = u"Если Вы уверены, что не хотите указывать эту информацию"
        self.assertBodyTextPresent(are_you_sure)

        person.input(favourites=favourites, ank_mode=True)
        self.ensure_not_submitted("Achievements were not filled")
        self.assertBodyTextPresent(are_you_sure)

        person.input(achievements=achievements, ank_mode=True)
        self.ensure_not_submitted("Hobbies were not filled")
        self.assertBodyTextPresent(are_you_sure)

        # and now fill last optional field and erase one of very important fields.
        person.input(
            last_name="",
            hobby=hobby,
            ank_mode=True,
        )
        self.ensure_not_submitted("Empty last name is not allowed. ")
        self.assertBodyTextPresent(last_name_too_short)

        # fill it again.
        person.input(
            last_name=u"НаученныйГорькимОпытом" + random_crap.random_text(5),
            hobby="",
            ank_mode=True,
        )
        self.ensure_not_submitted("Hobbies were erased")
        self.assertBodyTextPresent(are_you_sure)

        # now erase achievements.
        person.input(
            achievements="",
            ank_mode=True,
        )
        self.ensure_not_submitted(
            "Enter confirmation mode with erased field 'A' "
            "and remove another field 'B'. Revalidation check after bug #529"
        )
        person.input(
            hobby=hobby,
            achievements=achievements,
            ank_mode=True,
        )

        # now login as manager
        self.performLoginAsManager()

        self.gotoRoot()

        self.gotoUrlByLinkText(self.getAnketaListMenuName())

        # try to drill-down into table with new anketa.
        self.gotoUrlByLinkText(person.short_alias())

        # just check text is on the page.
        logging.info("Checking that all filled fields are displayed on the page. ")
        self.checkPersonAliasInPersonView(person.full_alias())

        self.assertBodyTextPresent(person.birth_date)
        self.assertBodyTextPresent(person.school)
        self.assertBodyTextPresent(person.school_city)
        self.assertBodyTextPresent(person.ank_class)
        self.assertBodyTextPresent(person.phone)
        self.assertBodyTextPresent(person.cellular)
        self.assertBodyTextPresent(person.email)
        self.assertBodyTextPresent(person.skype)
        self.assertBodyTextPresent(social_profile_show)
        self.clickElementById("show-extra-person-info")
        self.wait(1)
        self.assertElementSubTextById("extra-person-info", favourites)
        self.assertElementSubTextById("extra-person-info", achievements)
        self.assertElementSubTextById("extra-person-info", hobby)
