#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmBulkActions(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks various bulk actions (archiving, class raising)
    """

    def run(self):
        self.test_bulk_archive()
        self.test_increase_class()

    def test_bulk_archive(self):
        # positive part: check that button is accessible by admin and works
        self.test_bulk_archive_impl(admin_mode=True)
        # negative part: check that button does not work in non-privileged mode
        self.test_bulk_archive_impl(admin_mode=False)

    def test_increase_class(self):
        # positive part: check that button is accessible by admin and works
        self.test_increase_class_impl(admin_mode=True)
        # negative part: check that button does not work in non-privileged mode
        self.test_bulk_archive_impl(admin_mode=False)

    def _login_as_admin_or_manager(self, admin_mode):
        if admin_mode:
            self.perform_login_as_admin()
        else:
            self.perform_login_as_manager()

    def test_bulk_archive_impl(self, admin_mode):
        self.ensure_logged_off()
        self.goto_root()
        self._login_as_admin_or_manager(admin_mode)
        self.goto_root()
        self.goto_xsm()
        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        person = xsm.Person(self)
        person.input(
            last_name=u"Архивариус",
            first_name=u"Пётр",
            patronymic=u"Семёнович",
            anketa_status="declined",
            random=True,
        )
        person.back_to_person_view()
        self.assertElementTextById("anketa_status-span", u"Отклонён")
        self.goto_xsm_anketas()

        self.clickElementById("bulk_archive-submit")
        self.wait(5, "Wait while form resubmits")
        self.check_page_errors()

        self.goto_xsm_anketas()
        if admin_mode:
            self.assertTextNotPresent(
                xpath="//span[@class='anketa-status xe-declined']",
                text=u"Отклонён",
            )
        else:
            self.assertTextPresent(
                xpath="//span[@class='anketa-status xe-declined']",
                text=u"Отклонён",
            )

    def test_increase_class_impl(self, admin_mode):
        self.ensure_logged_off()
        self.goto_root()
        self._login_as_admin_or_manager(admin_mode)
        self.goto_root()
        self.goto_xsm()
        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        raisable_person = xsm.Person(self)
        raisable_person.input(
            last_name=u"Классный",
            first_name=u"Увеличитель",
            patronymic=u"Петрович",
            ank_class=u"7",
            current_class=u"8",
            anketa_status="cont",
            department_id=1,  # поднимаем только физиков пока что
            is_student=True,  # raise only scholars
            random=True,
        )
        raisable_person.back_to_person_view()

        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        non_raisable_person = xsm.Person(self)
        non_raisable_person.input(
            last_name=u"Классный",
            first_name=u"Подросток",
            patronymic=u"Выпускнович",
            ank_class=u"10",
            current_class=u"11",
            anketa_status="cont",
            department_id=1,  # поднимаем только физиков пока что
            is_student=True,  # raise only scholars
            random=True,
        )
        non_raisable_person.back_to_person_view()

        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        non_raisable_teacher = xsm.Person(self)
        non_raisable_teacher.input(
            last_name=u"Препод",
            first_name=u"Склассом",
            patronymic=u"Забытович",
            ank_class=u"10",
            current_class=u"3курс",
            anketa_status="cont",
            department_id=1,  # поднимаем только физиков пока что
            is_teacher=True,  # should not be raised
            random=True,
        )
        non_raisable_teacher.back_to_person_view()
        self.goto_xsm_all_people()
        self.clickElementById("increase_class_numbers-submit")
        self.wait(5, "Wait while form resubmits")
        self.check_page_errors()
        if admin_mode:
            # FIXME: wtf??? two commands for link title navigation???
            list_href = self.get_url_by_link_data(u"Вернуться к списку")

        self.gotoSite(list_href)

        self.anketa_drilldown(raisable_person, do_login=False, drilldown_to=xsm.DrilldownTo.ALL_LIST)
        current_class = self.getElementTextById("span-person_current_class")
        if admin_mode:
            self.assert_equal(current_class, "9", "Class was not raised from 8 to 9. ")
        else:
            self.assert_equal(current_class, "8", "Class should remain the same in non-admin mode. ")

        # test 11 class scholar
        self.goto_xsm_all_people()
        self.anketa_drilldown(non_raisable_person, do_login=False, drilldown_to=xsm.DrilldownTo.ALL_LIST)
        current_class = self.getElementTextById("span-person_current_class")
        if admin_mode:
            self.assert_equal(current_class, "n/a", "Class should be n/a. ")
        else:
            self.assert_equal(current_class, "11", "Class should remain the same in non-admin mode, not n/a. ")

        # test non-scholar (same effect for both admin/non-admin mode)
        self.goto_xsm_all_people()
        self.anketa_drilldown(non_raisable_teacher, do_login=False, drilldown_to=xsm.DrilldownTo.ALL_LIST)
        current_class = self.getElementTextById("span-person_current_class")
        self.assert_equal(current_class, u"3курс", "Teachers should not be raised. ")
