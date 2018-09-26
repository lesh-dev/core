#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmCourseWithoutLecturer(xsm.Manager, xtest_common.XcmsTest):
    """
    #888 test case

    creating school
    creating teacher
    creating course
    deleting teacher for this course

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
            last_name=u"Мертвая",
            first_name=u"Душа",
            patronymic=u"препода",
            random=True,
            is_teacher=True,
        )
        teacher.back_to_person_view()
        teacher.add_to_school(school)

        self.assertBodyTextPresent(u"Курсы")

        course = self.add_course_to_teacher(teacher)

        self.goto_xsm_courses()
        self.gotoUrlByLinkText(course.course_title)
        self.gotoUrlByLinkText(u"Редактировать преподов")
        self.clickElementById('delete-teacher-submit')
        self.goto_xsm_courses()
        self.assertPhpErrors()
