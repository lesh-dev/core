#!/usr/bin/python
# -*- coding: utf8 -*-

import re
import logging

import xsm
import xtest_common
import random_crap


class XcmsXsmCourseWithMultipleTeachers(xtest_common.XcmsTest):
    """
    This test checks course add functional.
    Steps:
    * login as manager
    * add new school
    * add 3 new teachers
    * add course on this new school
    * populate teacher list
    """

    def add_teacher(self):
        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()
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
        self.gotoXsm()
        school = xsm.add_test_school(self)

        self.add_teacher()
        self.add_teacher()
        self.add_teacher()

        self.gotoXsmCourses()
        self.gotoUrlByLinkText(school.school_title)
        self.gotoXsmAddCourse()

        inpCourseName = u"Многопреподный Курс " + random_crap.randomCrap(4)
        inpCourseName = self.fillElementByName("course_title", inpCourseName)
        inpTargetClass = "7-11"
        inpTargetClass = self.fillElementByName("target_class", inpTargetClass)

        inpDescription = u"Описание многопреподного курса " + random_crap.randomCrap(5, ["multiline"])
        inpDescription = self.fillElementByName("course_desc", inpDescription)

        inpComment = u"Комментарий к курсу " + random_crap.randomCrap(4, ["multiline"])
        inpComment = self.fillElementByName("course_comment", inpComment)

        id1, teacher1 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        id2, teacher2 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 2)
        id3, teacher3 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 3)

        teacher1 = self.filter_teacher_name(teacher1)
        teacher2 = self.filter_teacher_name(teacher2)
        teacher3 = self.filter_teacher_name(teacher3)

        logging.info("Teacher 1: '%s'", teacher1)
        logging.info("Teacher 2: '%s'", teacher2)
        logging.info("Teacher 3: '%s'", teacher3)

        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)

        self.clickElementByName("update-course")
        self.gotoBackToCourseView()
        self.assertUrlPresent(teacher1)

        self.gotoUrlByLinkText(u"Редактировать преподов")

        self.assertUrlPresent(teacher1)

        # after teacher1 is removed from list, teacher2 should take his place.
        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        self.assertUrlPresent(teacher1)
        self.assertUrlPresent(teacher2)

        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        self.assertUrlPresent(teacher1)
        self.assertUrlPresent(teacher2)
        self.assertUrlPresent(teacher3)

        self.gotoUrlByLinkText(u"Вернуться к просмотру курса")

        self.assertUrlPresent(teacher1)
        self.assertUrlPresent(teacher2)
        self.assertUrlPresent(teacher3)
