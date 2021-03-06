#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmAddCourses(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks course add functional.
    It does following:
    * login as XSM manager
    * enter 'all people list'
    * add new person
    * add person to some school
    * add some courses to this person
    """

    def run(self):
        self.ensure_logged_off()
        self.perform_login_as_manager()
        self.goto_xsm()
        school = xsm.add_test_school(self)

        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        teacher = xsm.Person(self)
        teacher.input(
            last_name=u"Преподов",
            first_name=u"Александр",
            patronymic=u"Ильич",
            random=True,
            is_teacher=True,
        )
        teacher.back_to_person_view()
        teacher.add_to_school(school)

        self.assertBodyTextPresent(u"Курсы")

        for i in range(0, 3):
            self.add_course_to_teacher(teacher)
