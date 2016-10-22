#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

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

    def add_exams_by_id(self, exam_ids):
        for exam in exam_ids:
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

            exam_comment = u"Коммент к сданному зачёту: " + random_crap.random_text(6)
            self.fillElementByName("exam_comment", exam_comment)
            self.clickElementByName("update-exam")
            self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Сдан")

    def set_exam_not_passed(self, exam_line_list):
        for examLine in exam_line_list:
            # <a><span>Прослушан</span></a>
            self.gotoIndexedUrlByLinkText(self.listened_status, examLine, "span")
            self.setOptionValueByIdAndValue("exam_status-selector", "notpassed")

            exam_comment = u"Коммент к несданному зачёту: " + random_crap.random_text(6)
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

        # add two teachers: 1st with 2 and 2nd with 3 courses
        teachers = []
        for ti in [1, 2]:
            self.gotoXsmAllPeople()
            self.gotoXsmAddPerson()
            teacher = xsm.Person(self)
            teacher.input(
                last_name=u"Препод_{}ый".format(ti),
                first_name=u"Александр" if ti == 1 else u"Иван",
                patronymic=u"Ильич" if ti == 1 else u"Петрович",
                random=True,
                is_teacher=True,
            )
            teacher.back_to_person_view()
            teacher.add_to_school(school)

            self.assertBodyTextPresent(u"Курсы")

            courses = [xsm.add_course_to_teacher(self, teacher) for _ in range(0, 1 + ti)]
            # store as custom property
            teacher.courses = courses

            teachers.append(teacher)

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

        self.assertBodyTextPresent(u"Зачёты")

        course_ids = []
        for teacher in teachers:
            for course in teacher.courses:
                course_ids.append(course.course_id)
        logging.info(course_ids)

        # take some id
        dup_id = course_ids[3]
        self.add_exams_by_id(course_ids)

        self.set_exam_passed([1, 2, 2])
        self.set_exam_not_passed([1, 0])

        # test duplicate exam
        self.add_exam_by_id(dup_id)
        self.assertBodyTextPresent(self.get_exam_already_exists_message())
