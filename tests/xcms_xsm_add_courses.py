#!/usr/bin/python
# -*- coding: utf8 -*-

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
    * add some courses
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

        self.performLoginAsManager()

        self.gotoAllPeople()
        self.gotoAddPerson()

        # generate
        inpLastName = u"Преподов_" + random_crap.randomText(5)
        inpFirstName = u"Александр_" + random_crap.randomText(3)
        inpMidName = u"Ильич_" + random_crap.randomText(3)
        
        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)

        # set student flag
        self.clickElementById("is_teacher-checkbox")

        self.clickElementById("update-person-submit")

        self.gotoBackToPersonView()

        fullAlias = xtest_common.fullAlias(inpLastName, inpFirstName, inpMidName)
        # check if person alias is present (person saved correctly)

        self.checkPersonAliasInPersonView(fullAlias)

        self.gotoUrlByLinkText(self.m_conf.getTestSchoolName())
        self.assertBodyTextPresent(self.getPersonAbsenceMessage())
        self.gotoUrlByLinkText(u"Зачислить на " + self.m_conf.getTestSchoolName())
        self.clickElementByName("update-person_school")
        self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Курсы")

        for i in range(0, 3):
            self.addCourse(xtest_common.shortAlias(inpLastName, inpFirstName))
