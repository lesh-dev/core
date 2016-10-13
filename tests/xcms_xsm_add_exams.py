#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
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
    listened_status = None

    @staticmethod
    def get_exam_already_exists_message():
        return u"Зачёт по этому курсу уже имеется"

    def add_exams_by_id(self, examIdList):
        for exam in examIdList:
            self.add_exam_by_id_and_return(exam)

    def add_exam_by_id_and_return(self, exam):
        self.add_exam_by_id(exam)
        self.assertBodyTextNotPresent(self.get_exam_already_exists_message())
        self.gotoBackToPersonView()

    def add_exam_by_id(self, exam):
        self.gotoUrlByLinkText(u"Добавить зачёт")
        self.setOptionValueByIdAndValue("course_id-selector", exam)
        self.clickElementByName("update-exam")

    def set_exam_passed(self, exam_line_list):
        for examLine in exam_line_list:
            # <a><span>Прослушан</span></a>
            self.gotoIndexedUrlByLinkText(self.listened_status, examLine, "span")
            self.setOptionValueByIdAndValue("exam_status-selector", "passed")

            exam_comment = u"Коммент к сданному зачёту: " + random_crap.randomText(6)
            self.fillElementByName("exam_comment", exam_comment)
            self.clickElementByName("update-exam")
            self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Сдан")

    def set_exam_not_passed(self, exam_line_list):
        for examLine in exam_line_list:
            # <a><span>Прослушан</span></a>
            self.gotoIndexedUrlByLinkText(self.listened_status, examLine, "span")
            self.setOptionValueByIdAndValue("exam_status-selector", "notpassed")

            exam_comment = u"Коммент к несданному зачёту: " + random_crap.randomText(6)
            self.fillElementByName("exam_comment", exam_comment)
            self.clickElementByName("update-exam")
            self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Не сдан")

    def run(self):
        self.ensure_logged_off()

        self.listened_status = u"Прослушан"

        self.performLoginAsManager()
        self.gotoXsm()
        school = xsm.add_test_school(self)

        self.gotoXsmAllPeople()
        self.gotoXsmAddPerson()
        student = xsm.Person(self)
        student.input(
            last_name=u"Зачётов",
            first_name=u"Андрей",
            patronymic=u"Михалыч",
            random=True,
            is_student=True,
        )
        student.back_to_person_view()
        student.add_to_school(school)

        # <option  value="95">Базовое электричество &#8212; Тараненко Сергей</option>
        # <option  value="134">Биомеханика &#8212; Преподаватель Другого</option>
        # <option  value="83">Ботаника &#8212; Преподаватель Другого</option>
        # <option  value="73">Введение в технику эксперимента &#8212; Пюрьбеева Евгения</option>
        # <option  value="119">Введение в химию &#8212; Марьясина Софья</option>
        # <option  value="101">Видеосъёмка &#8212; Дюно-Люповецкий Влас</option>
        # <option  value="137">Генетические алгоритмы &#8212; Мироненко-Маренков Антон</option>
        # <option  value="91">Геометрическая оптика &#8212; Пилипюк Дарья</option>

        self.assertBodyTextPresent(u"Зачёты")

        dup_id = 134

        self.add_exams_by_id([95, 119, 91, 73, 107, 130, 133, dup_id])

        self.set_exam_passed([1, 2, 2])
        self.set_exam_not_passed([1, 2, 2])

        # test duplicate exam
        self.add_exam_by_id(dup_id)
        self.assertBodyTextPresent(self.get_exam_already_exists_message())
