#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

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
        self.gotoXsm()
        self.gotoXsmSchools()

        # determine next year
        year = 2016
        page_content = self.getPageContent()
        while str(year) in page_content:
            year += 1
        logging.info("Found year that is not present on this page: %s", year)
        self.gotoXsmAddSchool()

        # generate school number
        school = xsm.School(self)
        school.input(
            school_title=u"ЛЭШ" + str(year),
            school_date_start=str(year) + ".07.15",
            school_date_end=str(year) + ".08.15",
            school_location=u"Деревня Гадюкино",
            random=True,
        )
        school.back_to_school_view()

        self.gotoUrlByLinkText(u"Правка")

        school.input(
            school_date_start=str(year) + ".07.23",
            school_date_end=str(year) + ".08.23",
        )
        school.back_to_school_view()

