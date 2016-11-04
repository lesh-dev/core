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

    # with string repr
    cellular = None
    cellular_list = None

    # with string repr
    phone = None
    phone_list = None

    birth_date = None
    school = None
    school_city = None
    ank_class = None
    current_class = None
    email = None
    skype = None
    social_profile = None
    favourites = None
    achievements = None
    hobby = None
    lesh_ref = None
    # not a database property
    control_question = None
    # in-school properties
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
        birth_date=None,
        school=None,
        school_city=None,
        ank_class=None,
        current_class=None,
        cellular_list=None,
        cellular=None,
        phone=None,
        phone_list=None,
        email=None,
        skype=None,
        social_profile=None,
        favourites=None,
        achievements=None,
        hobby=None,
        lesh_ref=None,
        control_question=None,
        is_student=False,
        is_teacher=False,
        # options
        random=False,
        ank_mode=False,
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

        if cellular_list is not None:
            self.cellular = ", ".join(cellular_list)
            self.cellular_list = list(map(self.phone_fix, cellular_list))
            self.cellular = t.fillElementById("cellular-input", self.cellular)
        elif cellular is not None:
            self.cellular_list = [cellular]
            self.cellular = t.fillElementById("cellular-input", cellular)

        if phone_list is not None:
            self.phone = ", ".join(phone_list)
            self.phone_list = list(map(self.phone_fix, phone_list))
            self.phone = t.fillElementById("phone-input", self.phone)
        elif phone is not None:
            self.phone_list = [phone]
            self.phone = t.fillElementById("phone-input", phone)

        if birth_date is not None:
            self.birth_date = t.fillElementById("birth_date-input", birth_date)

        if school is not None:
            self.school = t.fillElementById("school-input", school)

        if school_city is not None:
            self.school_city = t.fillElementById("school_city-input", school_city)

        if ank_class is not None:
            self.ank_class = t.fillElementById("ank_class-input", ank_class)

        if current_class is not None:
            self.current_class = t.fillElementById("current_class-input", current_class)

        if email is not None:
            self.email = t.fillElementById("email-input", email)

        if skype is not None:
            self.skype = t.fillElementById("skype-input", skype)

        if social_profile is not None:
            self.social_profile = t.fillElementById("social_profile-input", social_profile)

        if achievements is not None:
            self.achievements = t.fillElementById("achievements-text", achievements)

        if favourites is not None:
            self.favourites = t.fillElementById("favourites-text", favourites)

        if hobby is not None:
            self.hobby = t.fillElementById("hobby-text", hobby)

        if lesh_ref is not None:
            self.lesh_ref = t.fillElementById("lesh_ref-text", lesh_ref)

        if control_question is not None:
            self.control_question = t.fillElementById("control_question-input", control_question)

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

        # TODO(mvel): autodetect!
        if ank_mode:
            t.clickElementById("submit_anketa-submit")
        else:
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
    course_id = None
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
                course_title += "_" + rc.randomCrap(4)
            self.course_title = t.fillElementByName("course_title", course_title)

        if target_class is not None:
            self.target_class = t.fillElementByName("target_class", target_class)

        if course_desc is not None:
            course_desc += " " + rc.randomCrap(10, ["multiline"])
            self.course_desc = t.fillElementByName("course_desc", course_desc)

        if course_comment is not None:
            course_comment += " " + rc.randomCrap(10, ["multiline"])
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
                school_title += "_" + rc.randomWord(6)
            self.school_title = self.xtest.fillElementByName("school_title", school_title)

        if school_date_start is not None:
            self.school_date_start = self.xtest.fillElementByName("school_date_start", school_date_start)
            self.year = school_date_start[0:4]

        if school_date_end is not None:
            self.school_date_end = self.xtest.fillElementByName("school_date_end", school_date_end)

        if school_location is not None:
            if random:
                school_location += "_" + rc.randomWord(6)
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


def add_course_to_teacher(xtest, teacher):
    xtest.gotoUrlByLinkText(u"Добавить курс")
    course = Course(xtest)
    course.input(
        course_title=u"Курс",
        course_comment=u"Какой-то комментарий",
        course_desc=u"Описание курса",
        target_class=u"7-11",
        random=True,
    )
    # XSM BUG: we should return to teacher page, not to course page!
    xtest.gotoUrlByLinkText(u"Вернуться к просмотру")  # view of what? Course? no, teacher!
    course.course_id = int(xtest.getElementValueByName("course_id"))
    xtest.gotoUrlByLinkText(teacher.short_alias())
    return course
