#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmAnketaDuplicate(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks duplicate anketa add functional.
    * Adds anketa
    * Adds one more anketa with same name
    * Ensures it is duplicate
    * Ensures that duplicate is not shown
    * Submits anketa once more
    * Ensures that status was changed
    """

    @staticmethod
    def input_person_data(person):
        iteration = 0
        fmt = u"iteration {0}_{1}"
        crap_params = 15, ["multiline"]
        crap_func = random_crap.randomCrap
        crap_end = " CRAP_END"
        fav = crap_func(*crap_params) + crap_end
        ach = crap_func(*crap_params) + crap_end
        hob = crap_func(*crap_params) + crap_end
        src = crap_func(*crap_params) + crap_end

        person.input(
            # const fields
            last_name=person.last_name,
            first_name=u"Пётр",
            patronymic=u"Сергеевич",
            birth_date=random_crap.date(),
            phone=person.phone,
            cellular=person.cellular,
            email=person.email,
            # random crap that can vary from submission to submission
            school=u"Школа дубликатов № " + random_crap.randomDigits(4),
            school_city=u"Дублёво-" + random_crap.randomDigits(2),
            ank_class=random_crap.randomDigits(1) + u" Жэ",
            skype=random_crap.random_text(8),
            social_profile=random_crap.randomVkontakte(),
            favourites=fmt.format(iteration, fav),
            achievements=fmt.format(iteration, ach),
            hobby=fmt.format(iteration, hob),
            lesh_ref=fmt.format(iteration, src),
            control_question=u"Ампер",
            ank_mode=True,
        )

    def add_anketa(self, person):
        self.gotoRoot()
        self.goto_anketa()
        self.input_person_data(person)

    def check_unique_anketa(self, person):
        # login as admin
        self.performLoginAsManager()
        self.goto_xsm()
        self.goto_xsm_anketas()
        self.filter_person(fio=person.short_alias())
        self.assert_equal(
            self.countIndexedUrlsByLinkText(person.short_alias()), 1,
            "Found more than one anketa with exact FIO. Duplicate filtering is broken. "
        )

    def change_status(self, person):
        self.goto_xsm()
        self.goto_xsm_anketas()
        self.gotoUrlByLinkText(person.short_alias())
        self.goto_xsm_change_person_status()

        self.setOptionValueByIdAndValue("anketa_status-selector", "nextyear")
        comment_text = u"Меняем статус первой анкете: " + random_crap.randomCrap(5)
        comment_text = self.fillElementById("comment_text-text", comment_text)

        self.clickElementById("update-person_comment-submit")
        self.goto_back_to_person_view()

        new_state = u"Отложен"
        self.assertBodyTextPresent(u"Статус Новый изменён на {0}".format(new_state))
        self.assertBodyTextPresent(comment_text)

    def check_status(self, person):
        self.goto_xsm()
        self.goto_xsm_anketas()
        self.gotoUrlByLinkText(person.short_alias())
        # anketa should change status to new (like 'ticket reopen')
        self.assertElementTextById("anketa_status-span", u"Новый")

    def run(self):
        self.ensure_logged_off()
        person = xsm.Person(self)
        person.last_name = u"Дубликатов" + random_crap.random_text(5)
        person.phone = random_crap.phone()
        person.cellular = random_crap.phone()
        person.email = random_crap.email()

        self.add_anketa(person)
        self.assertBodyTextPresent(self.get_anketa_success_submit_message())
        self.add_anketa(person)
        self.assertBodyTextNotPresent(self.get_anketa_success_submit_message())
        self.assertBodyTextPresent(self.get_anketa_duplicate_submit_message())

        self.check_unique_anketa(person)

        self.change_status(person)

        self.add_anketa(person)
        self.assertBodyTextNotPresent(self.get_anketa_success_submit_message())
        self.assertBodyTextPresent(self.get_anketa_duplicate_submit_message())

        self.check_status(person)
