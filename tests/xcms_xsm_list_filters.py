#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmListFilters(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks various filters in XSM lists.
    """

    def check_filter(self, pattern, match_text, expected_count, message, extended_search=False):
        self.filter_person(fio=pattern)
        self.assert_equal(
            self.countIndexedUrlsByLinkText(match_text), expected_count,
            message + "Filters are broken. "
        )
        if extended_search:
            self.assertBodyTextPresent(u"Условия фильтрации были ослаблены")

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
        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
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

        self.goto_xsm_all_people()
        self.setOptionValueByIdAndValue("show_department_id-selector", department_id)
        alias = person.short_alias()
        self.check_filter(alias, alias, 1, "Search with proper department selection return 1 record. ")

        other_department_id = 2  # Другое
        self.setOptionValueByIdAndValue("show_department_id-selector", other_department_id)
        self.check_filter(
            alias, alias, 1,
            "Search with wrong department should return 1 records with hint about extended search.  ",
            extended_search=True,
        )

    def test_comments(self):
        # TODO(mvel): в этом месте несколько раз всплывала бага, что текст комментария
        # двоится. Надо добавить код, проверяющий, что этот текст встречается 1 раз на странице.
        self.goto_xsm_all_people()
        self.clear_filters()

        comment_was_set = False
        person = xsm.Person(self)
        # FIXME(mvel): очень неудобный инструментарий работы с checkbox-ами. Нет интерфейса
        # "убедиться, что включено". Надо его добавить и потом проверять, что комментарии есть
        # только тогда, когда включено.
        for i in xrange(2):
            if self.checkBodyTextPresent(u"Добавить комментарий"):
                comment_was_set = True
                comment_text = person.add_comment()
                self.goto_xsm_all_people()
                self.checkBodyTextPresent(comment_text)

            self.clickElementById("show_comments-checkbox")
            self.wait(3, "Wait while form resubmits")
            self.check_page_errors()

        self.assert_equal(comment_was_set, True, "No comment can be added: no links. ")

    def run(self):
        self.ensure_logged_off()

        self.perform_login_as_manager()
        self.goto_root()
        self.goto_xsm()
        self.goto_xsm_all_people()

        self.test_existing_people()
        self.test_department_selector()
        self.test_comments()
