#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsXsmAddExams(xtest_common.XcmsTest):
    """
    This test checks exam add functional.
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * add person to some school
    * add some courses
    * set exam status
    """
    
    def getExamAlreadyExistsMessage(self):
        return u"Зачёт по этому курсу уже имеется"
    
    def addExamsById(self, examIdList):
        for exam in examIdList:
            self.addExamByIdAndReturn(exam)

    def addExamByIdAndReturn(self, exam):
        self.addExamById(exam)
        self.assertBodyTextNotPresent(self.getExamAlreadyExistsMessage())
        self.gotoBackToPersonView()

    def addExamById(self, exam):
        self.gotoUrlByLinkText(u"Добавить зачёт")
        self.setOptionValueByIdAndValue("course_id-selector", exam)
        self.clickElementByName("update-exam")

    def setExamPassed(self, examLineList):
        for examLine in examLineList:
            # <a><span>Прослушан</span></a>
            self.gotoIndexedUrlByLinkText(self.m_listenedStatus, examLine, "span")
            self.setOptionValueByIdAndValue("exam_status-selector", "passed")

            examComment = u"Коммент к сданному зачёту: " + random_crap.randomText(6)
            self.fillElementByName("exam_comment", examComment)
            self.clickElementByName("update-exam")
            self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Сдан")

    def setExamNotPassed(self, examLineList):
        for examLine in examLineList:
            # <a><span>Прослушан</span></a>
            self.gotoIndexedUrlByLinkText(self.m_listenedStatus, examLine, "span")
            self.setOptionValueByIdAndValue("exam_status-selector", "notpassed")

            examComment = u"Коммент к несданному зачёту: " + random_crap.randomText(6)
            self.fillElementByName("exam_comment", examComment)
            self.clickElementByName("update-exam")
            self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Не сдан")

    def run(self):

        self.m_listenedStatus = u"Прослушан"

        self.performLoginAsManager()
        self.gotoXsmAllPeople()

        self.gotoXsmAddPerson()

        # generate
        inpLastName = u"Зачётов" + random_crap.randomText(5)
        inpFirstName = u"Андрей_" + random_crap.randomText(3)
        inpMidName = u"Михалыч_" + random_crap.randomText(3)

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)

        # set student flag
        self.clickElementById("is_student-checkbox")

        self.clickElementById("update-person-submit")

        self.gotoBackToPersonView()

        fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
        # check if person alias is present (person saved correctly)
        self.checkPersonAliasInPersonView(fullAlias)

        self.gotoUrlByLinkText(self.m_conf.getTestSchoolName())
        self.assertBodyTextPresent(self.getPersonAbsenceMessage())
        self.gotoUrlByLinkTitle(u"Зачислить на " + self.m_conf.getTestSchoolName())
        self.clickElementByName("update-person_school")
        self.gotoBackToPersonView()

        #<option  value="95">Базовое электричество &#8212; Тараненко Сергей</option>
        #<option  value="134">Биомеханика &#8212; Преподаватель Другого</option>
        #<option  value="83">Ботаника &#8212; Преподаватель Другого</option>
        #<option  value="73">Введение в технику эксперимента &#8212; Пюрьбеева Евгения</option>
        #<option  value="119">Введение в химию &#8212; Марьясина Софья</option>
        #<option  value="101">Видеосъёмка &#8212; Дюно-Люповецкий Влас</option>
        #<option  value="137">Генетические алгоритмы &#8212; Мироненко-Маренков Антон</option>
        #<option  value="91">Геометрическая оптика &#8212; Пилипюк Дарья</option>

        self.assertBodyTextPresent(u"Зачёты")

        dupId = 134
        
        self.addExamsById([95, 119, 91, 73, 107, 130, 133, dupId])

        self.setExamPassed([1, 2, 2])
        self.setExamNotPassed([1, 2, 2])

        # test duplicate exam
        self.addExamById(dupId)
        self.assertBodyTextPresent(self.getExamAlreadyExistsMessage())
        
