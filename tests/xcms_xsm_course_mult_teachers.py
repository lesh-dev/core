#!/usr/bin/python
# -*- coding: utf8 -*-

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

    def addSchool(self):
        self.gotoXsmSchools()
        self.gotoXsmAddSchool()

        # generate school number
        lastDigit = random_crap.randomDigits(1)

        inpSchoolTitle = u"ЛЭШ_205{0}_".format(lastDigit) + random_crap.randomWord(6);
        inpStart = "205{0}.07.15".format(lastDigit)
        inpEnd = "205{0}.08.16".format(lastDigit)

        inpSchoolTitle = self.fillElementByName("school_title", inpSchoolTitle)
        inpStart = self.fillElementByName("school_date_start", inpStart)
        inpEnd = self.fillElementByName("school_date_end", inpEnd)

        self.m_schoolTitle = inpSchoolTitle

        self.clickElementByName("update-school")
        self.gotoBackToSchoolView()
        self.assertBodyTextPresent(inpSchoolTitle)

    def addTeacher(self):
        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()

        # generate prepod name - to be first in list
        inpLastName = u"Мультипреподов_" + random_crap.randomText(4)
        inpFirstName = u"Сергей_" + random_crap.randomText(3)
        inpMidName = u"Викторович_" + random_crap.randomText(3)

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

    def filterTeacherName(self, name):
        if name.startswith("("):
            return name[3:]
        return name
    
    def run(self):

        self.performLoginAsManager()
        self.gotoXsm()
        
        self.addSchool()
        
        self.addTeacher()
        self.addTeacher()
        self.addTeacher()

        self.gotoXsmCourses()
        self.gotoUrlByLinkText(self.m_schoolTitle)
        self.gotoXsmAddCourse()

        inpCourseName = u"Многопреподный Курс " + random_crap.randomCrap(4)
        inpCourseName = self.fillElementByName("course_title", inpCourseName)
        inpTargetClass = "7-11"
        inpTargetClass = self.fillElementByName("target_class", inpTargetClass)

        inpDescription = u"Описание многопреподного курса " + random_crap.randomCrap(5, ["multiline"])
        inpDescription = self.fillElementByName("course_desc", inpDescription)

        inpComment = u"Комментарий к курсу " + random_crap.randomCrap(4, ["multiline"])
        inpComment = self.fillElementByName("course_comment", inpComment)

        teacher1 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        teacher2 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 2)
        teacher3 = self.getOptionValueByIdAndIndex("course_teacher_id-selector", 3)
        
        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)

        self.clickElementByName("update-course")
        self.gotoBackToCourseView()
        self.assertUrlPresent(self.filterTeacherName(teacher1))
        
        self.gotoUrlByLinkText(u"Редактировать преподов")
        
        self.assertUrlPresent(self.filterTeacherName(teacher1))
        
        # after first prepod removed from list, teacher2 should take his place.
        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        self.assertUrlPresent(self.filterTeacherName(teacher1))
        self.assertUrlPresent(self.filterTeacherName(teacher2))

        self.setOptionValueByIdAndIndex("course_teacher_id-selector", 1)
        self.clickElementByName("add-teacher")
        self.assertUrlPresent(self.filterTeacherName(teacher1))
        self.assertUrlPresent(self.filterTeacherName(teacher2))
        self.assertUrlPresent(self.filterTeacherName(teacher3))

        self.gotoUrlByLinkText(u"Вернуться к просмотру курса")

        self.assertUrlPresent(self.filterTeacherName(teacher1))
        self.assertUrlPresent(self.filterTeacherName(teacher2))
        self.assertUrlPresent(self.filterTeacherName(teacher3))
        