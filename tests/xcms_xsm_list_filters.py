#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmListFilters(xtest_common.XcmsTest):
    """
    This test checks various filters in XSM lists.
    """
    fio_filter_id = "show_name_filter-input"

    def check_filter(self, pattern, match_text, expected_count, message):
        self.fillElementById(self.fio_filter_id, pattern)
        self.clickElementByName("show-person")
        self.assert_equal(
            self.countIndexedUrlsByLinkText(match_text), expected_count,
            message + "Filters are broken. "
        )

    def test_existing_people(self):
        # one line expected
        self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        person = xsm.Person(self)
        person.last_name = u"Вельтищев"
        person.first_name = u"Михаил"
        person.patronymic = u"Николаевич"
        self.check_filter(
            person.full_alias(), person.short_alias(), 1,
            "Found more than one anketa with exact FIO. "
        )

        # 2 lines expected
        short_aliases = [
            u"Вельтищев Михаил",
            u"Вельтищев Дмитрий",
        ]
        alias = u"Вельтищев"
        for short_alias in short_aliases:
            self.check_filter(alias, short_alias, 1, u"Expected link {} not found. ".format(short_alias))

        # none lines expected
        alias = "qwerty"
        self.check_filter(alias, alias, 0, "This search should return nothing. ")

        # 1 line expected
        alias = u"Демарин Дмитрий"
        self.check_filter(alias, alias, 1, "This search should return one record. ")

    def test_department_selector(self):
        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()
        department_id = 3  # Математическое
        person = xsm.Person(self)
        person.input(
            last_name=u"Гуглов",
            first_name=u"Индекс",
            patronymic=u"Яхович",
            department_id=department_id,
            is_student=True,
            random=True,
        )
        person.back_to_person_view()

        self.gotoXsmAllPeople()
        self.setOptionValueByIdAndValue("show_department_id-selector", department_id)
        alias = person.short_alias()
        self.check_filter(alias, alias, 1, "Search with proper department selection return 1 record. ")

        other_department_id = 2  # Другое
        self.setOptionValueByIdAndValue("show_department_id-selector", other_department_id)
        self.check_filter(alias, alias, 0, "Search with wrong department should return 0 records. ")

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()
        self.gotoRoot()
        self.gotoXsm()
        self.gotoXsmAllPeople()

        self.test_existing_people()
        self.test_department_selector()
