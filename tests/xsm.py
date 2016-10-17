# coding: utf-8

"""
    Here we (re)implement basic XSM entities in Python
    with generic testing abilities, as vstarodub@ done
    with Effi-based entities in ASoft.

    Achtung: PEP8 grammar_nazi is here. Do not use
    lowerCamelCase, CamelCase, etc.
"""

import logging
import random_crap as rc


class Person(object):
    """
        Иван Человеков был простой человек
        И просто смотрел на свет
        И "Да" его было настоящее "Да",
        А "Нет" -- настоящее "Нет"!

                    И. Кормильцев, В. Бутусов
    """
    # Parent test object
    xtest = None
    # Same namings as in XSM
    first_name = None
    last_name = None
    patronymic = None
    social_profile = None
    # with string repr
    cellular = None
    cellular_str = None
    # with string repr
    phone = None
    phone_str = None
    is_student = None
    is_teacher = None

    def __init__(self, xtest):
        self.xtest = xtest

    def input(
        self,
        department_id=None,
        first_name=None,
        last_name=None,
        patronymic=None,
        social_profile=None,
        cellular=None,
        phone=None,
        is_student=False,
        is_teacher=False,
        random=False,
    ):
        t = self.xtest
        if last_name is not None:
            if random:
                last_name += "_" + rc.random_text(5)

            self.last_name = t.fillElementById("last_name-input", last_name)

        if first_name is not None:
            if random:
                first_name += "_" + rc.random_text(3)
            self.first_name = t.fillElementById("first_name-input", first_name)

        if patronymic is not None:
            if random:
                patronymic += "_" + rc.random_text(3)
            self.patronymic = t.fillElementById("patronymic-input", patronymic)

        if social_profile is not None:
            self.social_profile = t.fillElementById("social_profile-input", social_profile)

        if cellular is not None:
            self.cellular_str = ", ".join(cellular)
            self.cellular = list(map(self.phone_fix, cellular))
            self.cellular_str = t.fillElementById("cellular-input", self.cellular_str)

        if phone is not None:
            self.phone_str = ", ".join(phone)
            self.phone = list(map(self.phone_fix, phone))
            self.phone_str = t.fillElementById("phone-input", self.phone_str)

        if is_student is not None:
            self.is_student = is_student
            # FIXME(mvel): will not handle 'unchecked' option
            if is_student:
                t.clickElementById("is_student-checkbox")

        if is_teacher is not None:
            self.is_teacher = is_teacher
            # FIXME(mvel): will not handle 'unchecked' option
            if is_teacher:
                t.clickElementById("is_teacher-checkbox")

        if department_id is not None:
            t.setOptionValueByIdAndValue("department_id-selector", department_id)

        t.clickElementById("update-person-submit")

    def back_to_person_view(self):
        t = self.xtest
        # FIXME(mvel): this is a Person control: gotoBackToPersonView()
        t.gotoBackToPersonView()
        full_alias = self.full_alias()
        # check if person alias is present (person saved correctly)
        t.checkPersonAliasInPersonView(full_alias)

    def add_to_school(self, school):
        t = self.xtest
        t.gotoUrlByLinkText(school.school_title)
        t.assertBodyTextPresent(t.getPersonAbsenceMessage())
        t.gotoUrlByLinkTitle(u"Зачислить на " + school.school_title)
        t.clickElementByName("update-person_school")
        t.gotoBackToPersonView()

    def short_alias(self):
        short_alias = self.last_name + " " + self.first_name
        return short_alias.strip()

    def full_alias(self):
        full_alias = self.last_name + " " + self.first_name + " " + self.patronymic
        return full_alias.strip()

    @staticmethod
    def phone_fix(phone):
        return phone.replace("+7", "8").replace("8-900-", "8(900)")

    def get_row_value(self, person_id, field_name, subindex=None):
        if subindex is not None:
            ele_id = "person{0}-{1}-{2}".format(person_id, field_name, subindex)
        else:
            ele_id = "person{0}-{1}".format(person_id, field_name)
        return self.xtest.getElementTextById(ele_id)


class Course(object):
    # Parent test object
    xtest = None
    # Same namings as in XSM
    course_title = None
    target_class = None
    course_desc = None
    course_comment = None

    def __init__(self, xtest):
        self.xtest = xtest

    def input(
        self,
        course_title=None,
        target_class=None,
        course_desc=None,
        course_comment=None,
        random=False,
        update=True,
    ):
        t = self.xtest
        if course_title is not None:
            if random:
                course_title += rc.randomCrap(4)
            self.course_title = t.fillElementByName("course_title", course_title)

        if target_class is not None:
            self.target_class = t.fillElementByName("target_class", target_class)

        if course_desc is not None:
            course_desc += rc.randomCrap(10, ["multiline"])
            self.course_desc = t.fillElementByName("course_desc", course_desc)

        if course_comment is not None:
            course_comment += rc.randomCrap(10, ["multiline"])
            self.course_comment = t.fillElementByName("course_comment", course_comment)

        if update:
            t.clickElementByName("update-course")


class School(object):
    # Same namings as in XSM
    school_title = None
    school_date_start = None
    school_date_end = None
    school_location = None
    # helper
    year = None

    def __init__(self, xtest):
        self.xtest = xtest

    def input(
        self,
        school_title=None,
        school_date_start=None,
        school_date_end=None,
        school_location=None,
        random=False,
    ):
        if school_title is not None:
            if random:
                school_title += '_' + rc.randomWord(6)
            self.school_title = self.xtest.fillElementByName("school_title", school_title)

        if school_date_start is not None:
            self.school_date_start = self.xtest.fillElementByName("school_date_start", school_date_start)
            self.year = school_date_start[0:4]

        if school_date_end is not None:
            self.school_date_end = self.xtest.fillElementByName("school_date_end", school_date_end)

        if school_location is not None:
            if random:
                school_location += '_' + rc.randomWord(6)
            self.school_location = self.xtest.fillElementByName("school_location", school_location)

        self.xtest.clickElementByName("update-school")

    def back_to_school_view(self):
        self.xtest.gotoBackToSchoolView()
        self.xtest.assertBodyTextPresent(self.school_title)
        self.xtest.assertBodyTextPresent(self.school_date_start)
        self.xtest.assertBodyTextPresent(self.school_date_end)
        self.xtest.assertBodyTextPresent(self.school_location)


def add_test_school(xtest):
    xtest.gotoXsmSchools()
    # determine next year
    year = 2016
    page_content = xtest.getPageContent()
    while str(year) in page_content:
        year += 1
    logging.info("Found year that is not present on this page: %s", year)
    xtest.gotoXsmAddSchool()

    # generate school number
    school = School(xtest)
    school.input(
        school_title=u"ЛЭШ-" + str(year),
        school_date_start=str(year) + ".07.15",
        school_date_end=str(year) + ".08.15",
        school_location=u"Деревня Гадюкино",
        random=True,
    )
    school.back_to_school_view()
    # global context fix ;)
    xtest.m_conf.set_test_school_name(school.school_title)
    return school
