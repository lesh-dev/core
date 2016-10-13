#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmAddCourses(xtest_common.XcmsTest):
    """
    This test checks course add functional.
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * add person to some school
    * add some courses to this person
    """

    def addCourse(self, teacherAlias):
        self.gotoUrlByLinkText(u"Добавить курс")

        inpCourseName = u"Курс " + random_crap.randomCrap(4)
        inpCourseName = self.fillElementByName("course_title", inpCourseName)
        inpTargetClass = "7-11"
        inpTargetClass = self.fillElementByName("target_class", inpTargetClass)

        inpDescription = random_crap.randomCrap(10, ["multiline"])
        inpDescription = self.fillElementByName("course_desc", inpDescription)

        inpComment = random_crap.randomCrap(10, ["multiline"])
        inpComment = self.fillElementByName("course_comment", inpComment)

        self.clickElementByName("update-course")
        # XSM BUG: we should return to prepod page, not to course page!
        self.gotoUrlByLinkText(u"Вернуться к просмотру")  # view of what? Course? no, prepod!
        self.gotoUrlByLinkText(teacherAlias)

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsManager()
        self.gotoXsm()
        school = xsm.add_test_school(self)

        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()
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
            self.addCourse(teacher.short_alias())
