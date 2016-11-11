#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm

import xtest_common


class XcmsXsmAddSchool(xtest_common.XcmsTest):
    """
    This test checks school add functional.
    * login as manager
    * enter XSM
    * add new school
    * check school list
    * check school in panel
    * edit school properties and save
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsManager()
        self.goto_xsm()
        school = xsm.add_test_school(self)
        self.gotoUrlByLinkText(u"Правка")
        school.input(
            school_date_start=str(school.year) + ".07.23",
            school_date_end=str(school.year) + ".08.23",
        )
        school.back_to_school_view()
