#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmListSort(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks various sorting in XSM lists.
    """

    def check_filter(self, pattern, match_text, expected_count, message, extended_search=False):
        self.filter_person(fio=pattern)
        self.assert_equal(
            self.countIndexedUrlsByLinkText(match_text), expected_count,
            message + "Filters are broken. "
        )
        if extended_search:
            self.assertBodyTextPresent(u"Условия фильтрации были ослаблены")

    def run(self):
        self.ensure_logged_off()

        self.perform_login_as_manager()
        self.goto_root()
        self.goto_xsm()
        self.test_sort()

    def test_sort(self):
        self.goto_xsm_all_people()
        self.clear_filters()
        self.clickElementById("sort_by_person_id")
        self.wait(3, "Wait while form resubmits")
        self.check_page_errors()

        self.clickElementById("sort_by_last_name")
        self.wait(3, "Wait while form resubmits")
        self.check_page_errors()

        # test url sent by friend
        self.gotoUrl("/xsm/list-person-locator&show_sort_column=-last_name,-department_id")
        self.check_page_errors()

        # test another url sent by friend
        self.gotoUrl("/xsm/list-person-locator&show_sort_column=department_id,last_name")
        self.check_page_errors()

