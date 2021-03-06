#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap
import time
import logging
import selenium_test


class XcmsXsmInplaceEdit(xsm.Manager, xtest_common.XcmsTest):
    """
    #979
    Creating a new particiant with some forest status, changing his status, checking changes took place
    """

    def run(self):
        return
        # TODO(nata-skr): finish
        self.ensure_logged_off()

        # anketa fill positive test:
        # all fields are filled with correct values.
        self.goto_root()
        self.goto_anketa()

        person = xsm.Person(self)
        person.input(
            last_name=u"Ландау",
            first_name=u"Лев",
            patronymic=u"Давидович",
            birth_date=random_crap.date(),
            school=u"Тестовая школа им. В.Е.Бдрайвера №",
            school_city=u"Школа находится в /var/opt/" + random_crap.random_text(5),
            ank_class=random_crap.randomDigits(1) + u" Гэ",
            cellular="+7" + random_crap.randomDigits(9),
            phone="+7" + random_crap.randomDigits(9),
            email=random_crap.random_text(10) + "@" + random_crap.random_text(6) + ".ru",
            skype=random_crap.random_text(12),
            social_profile=random_crap.randomVkontakte(),
            favourites=random_crap.randomCrap(20, ["multiline"]),
            achievements=random_crap.randomCrap(15, ["multiline"]),
            hobby=random_crap.randomCrap(10, ["multiline"]),
            lesh_ref=random_crap.randomCrap(10, ["multiline"]),
            control_question=u"ампер",
            ank_mode=True,
        )
        self.assertBodyTextPresent(self.get_anketa_success_submit_message())
        # inp_social_show = bawlib.cut_http(person.social_profile)

        # now login as admin
        inp_last_name = person.last_name
        self.anketa_drilldown(person)
        # now, let's change anketa status to "Ждет собеседования"

        self.gotoEditPerson()

        # change anketa status and save it.
        self.setOptionValueByIdAndValue("anketa_status-selector", "progress")

        self.clickElementById("update-person-submit")

        self.assertBodyTextPresent(u"Участник успешно сохранён")

        self.gotoUrlByLinkText(u"Лес")

        # create new person
        """self.clickElementById("clear_forest-submit")
        self.gotoUrlByLinkText(u"Добавить участника")
        self.setOptionValueByIdAndValue("anketa_status-selector", "less")
        inp_first_name = u"Ричард" + random_crap.random_text(6)
        inp_last_name = u"Фейнман" + random_crap.random_text(6)

        inp_first_name = self.fillElementByName("first_name", inp_first_name)
        inp_last_name = self.fillElementByName("last_name", inp_last_name)

        self.setOptionValueByIdAndValue("forest_1-selector", "maybe")
        self.clickElementById("update-person-submit")
        self.assertBodyTextPresent(u"Участник успешно сохранён")

        self.gotoUrlByLinkText(u"Лес")"""

        self.filter_person(fio=inp_last_name)
        # self.assertBodyTextPresent(u"ХЗ")
        time.sleep(5)
        self.doubeClickElementById("p1-forest_1-span")
        val = selenium_test.get_value(self.getElementById("forest_1-selector"))
        if val != "undef":
            self.failTest("Incorrect value in forest selector")
        logging.info("Element value: {0}".format(val))
        self.setOptionValueByIdAndValue("forest_1-selector", "no")

        self.assertBodyTextPresent(u"Не идёт")
        time.sleep(5)
        self.doubeClickElementById("p1-forest_1-span")
        val = selenium_test.get_value(self.getElementById("forest_1-selector"))
        if val != "no":
            self.failTest("Incorrect value in forest selector")
        # self.assertBodyTextNotPresent(u"ХЗ")
