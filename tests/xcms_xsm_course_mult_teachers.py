#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import logging

import xsm
import xtest_common


class XcmsXsmCourseWithMultipleTeachers(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks course add functional.
    Steps:
    * login as XSM manager
    * add new school
    * add 3 new teachers
    * add course on this new school
    * populate teacher list
    """

    def add_teacher(self):
        self.goto_xsm_all_people()
        self.goto_xsm_add_person()
        teacher = xsm.Person(self)
        teacher.input(
            last_name=u"Мультипреподов",
            first_name=u"Сергей",
            patronymic=u"Викторович",
            random=True,
            is_teacher=True,
        )
        teacher.back_to_person_view()
        # FIXME(mvel): is it right that teacher was not added to school?
        # teacher.add_to_school(school)

    @staticmethod
    def filter_teacher_name(name):
        if name.startswith("("):
            return re.sub(r'\(.*?\) *', '', name)
        return name

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsManager()
        self.goto_xsm()
        school = xsm.add_test_school(self)

        self.add_teacher()
        self.add_teacher()
        self.add_teacher()

        self.goto_xsm_courses()
        self.gotoUrlByLinkText(school.school_title)
        self.goto_xsm_add_course()
        course = xsm.Course(self)
        course.input(
            course_title=u"Многопреподный курс",
            course_comment=u"Комментарий к курсу",
            course_desc=u"Описание многопредметного курса",
            target_class=u"7-11",
            random=True,
            update=False,
        )
        # add first 3 teachers
        teacher_ids = []
        teacher_names = []
        for i in [1, 2, 3]:
            teacher_id, teacher = self.getOptionValueByIdAndIndex("course_teacher_id-selector", i)
            teacher_ids.append(teacher_id)
            teacher = self.filter_teacher_name(teacher)
            logging.info("Teacher %s: '%s'", i, teacher)
            teacher_names.append(teacher)

        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        course.input(update=True)
        self.goto_back_to_course_view()
        self.assertUrlPresent(teacher_names[0])

        self.gotoUrlByLinkText(u"Редактировать преподов")

        self.assertUrlPresent(teacher_names[0])

        # after 1st teacher is removed from list, 2nd teacher should take his place.
        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        self.assertUrlPresent(teacher_names[0])
        self.assertUrlPresent(teacher_names[1])

        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        for teacher in teacher_names:
            self.assertUrlPresent(teacher)

        self.gotoUrlByLinkText(u"Вернуться к просмотру курса")

        for teacher in teacher_names:
            self.assertUrlPresent(teacher)
