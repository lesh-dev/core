#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmAnketaDupStress(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks duplicate anketa merging algorithm.
    """

    @staticmethod
    def input_person_data(person, iteration, random=False):
        fmt = u"iteration {0}_{1}"
        if not random:
            fav = "my_favourites"
            ach = "some_achievements"
            hob = "different_hobbies"
            src = "wtf_source"
        else:
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
            first_name=u"Егор",
            patronymic=u"Фёдорович",
            birth_date=random_crap.date(),
            phone=person.phone,
            cellular=person.cellular,
            email=person.email,
            # random crap that can vary from submission to submission
            school=u"Школа спамеров №",
            school_city=u"Спамерово",
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

    def add_anketa(self, person, iteration):
        self.goto_root()
        self.goto_anketa()
        self.input_person_data(person, iteration, random=True)

    def check_unique_anketa(self, person):
        # now login as admin
        person_alias = person.short_alias()

        self.perform_login_as_manager()
        self.goto_root()
        self.goto_xsm()
        self.goto_xsm_anketas()
        self.filter_person(fio=person_alias)
        self.assert_equal(
            self.countIndexedUrlsByLinkText(person_alias), 1,
            "Found more than one anketa with exact FIO. Duplicate filtering is broken. "
        )
        self.goto_root()
        self.performLogoutFromSite()

    def run(self):
        self.ensure_logged_off()
        person = xsm.Person(self)
        # set some const fields
        person.last_name = u"Спамеров" + random_crap.randomWord(5)
        person.phone = random_crap.phone()
        person.cellular = random_crap.phone()
        person.email = random_crap.email()

        for iteration in range(0, 5):
            self.add_anketa(person, iteration)
            if iteration == 0:
                self.assertBodyTextPresent(self.get_anketa_success_submit_message())
            else:
                self.assertBodyTextNotPresent(self.get_anketa_success_submit_message())
                self.assertBodyTextPresent(self.get_anketa_duplicate_submit_message())

        self.check_unique_anketa(person)
