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
        self.test_bulk_archive_impl()
        self.test_bulk_archive_impl(admin_mode=False)

    def test_bulk_archive_impl(self, admin_mode=True):
        self.ensure_logged_off()
        self.goto_root()
        if admin_mode:
            self.perform_login_as_admin()
        else:
            self.perform_login_as_manager()
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

    def test_increase_class(self):
        # TODO: implement
        return
        # positive part: check that button is accessible by admin and works
        self.ensure_logged_off()
        self.goto_root()
        self.goto_anketa()

        self.perform_login_as_admin()
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
        self.assertTextNotPresent(
            xpath="//table[class='ankList']",
            text=u"Отклонён",
        )
