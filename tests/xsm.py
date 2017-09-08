# coding: utf-8

"""
    Here we (re)implement basic XSM entities in Python
    with generic testing abilities, as vstarodub@ done
    with Effi-based entities in ASoft.

    Achtung: PEP8 grammar_nazi is here. Do not use
    lowerCamelCase, CamelCase, etc.
"""

import re
import logging
import random_crap as rc
import xtest_common as xc


class Person(object):
    """
        Иван Человеков был простой человек
        И просто смотрел на свет
        И "Да" его было настоящее "Да",
        А "Нет" -- настоящее "Нет"!

                    И. Кормильцев, В. Бутусов
    """

    def __init__(self, xtest):
        # Parent test object
        self.xtest = xtest

        # Same namings as in XSM
        self.first_name = None
        self.last_name = None
        self.patronymic = None

        # with string repr
        self.cellular = None
        self.cellular_list = None

        # with string repr
        self.phone = None
        self.phone_list = None

        self.birth_date = None
        self.school = None
        self.school_city = None
        self.ank_class = None
        self.current_class = None
        self.email = None
        self.skype = None
        self.social_profile = None
        self.favourites = None
        self.achievements = None
        self.hobby = None
        self.lesh_ref = None
        # not a database property
        self.control_question = None
        # in-school properties
        self.is_student = None
        self.is_teacher = None

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
        # FIXME(mvel): this is a Person control: goto_back_to_person_view()
        t.goto_back_to_person_view()
        full_alias = self.full_alias()
        # check if person alias is present (person saved correctly)
        t.checkPersonAliasInPersonView(full_alias)

    def add_to_school(self, school):
        t = self.xtest
        t.gotoUrlByLinkText(school.school_title)
        t.assertBodyTextPresent(t.getPersonAbsenceMessage())
        t.gotoUrlByLinkTitle(u"Зачислить на " + school.school_title)
        t.clickElementByName("update-person_school")
        t.goto_back_to_person_view()

    def add_comment(self):
        t = self.xtest
        t.gotoUrlByLinkText(u"Добавить комментарий")
        comment_text = rc.random_text(40) + "\n" + rc.random_text(50) + "\n" + rc.random_text(30)
        comment_text = t.fillElementByName("comment_text", comment_text)
        t.clickElementByName("update-person_comment")
        t.assertBodyTextPresent(u"Комментарий успешно сохранён")
        t.goto_back_to_anketa_view()
        return comment_text

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
    """
    Class representing school
    :var school_title:
        string: School name
    :var school_data_start:
        string: School start date
    :var school_date_end:
        string: School end date
    :var school_location:
        string: School location
    :var year:
        string: School year calculated as firs 4 digits of school_data_start
    :var id:
        integer: School id in database
    """

    # Same namings as in XSM
    school_title = None
    school_date_start = None
    school_date_end = None
    school_location = None
    # helper
    year = None
    id = None

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
        """

        :param school_title:
            string: School name
        :param school_date_start:
            string: School start date
        :param school_date_end:
            string: School end date
        :param school_location:
            string: School location
        :param random:
            boolean: if it is necessary to add _<random crap> to school_title
        :return: void
        """
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
        self.xtest.goto_back_to_school_view()
        self.xtest.assertBodyTextPresent(self.school_title)
        self.xtest.assertBodyTextPresent(self.school_date_start)
        self.xtest.assertBodyTextPresent(self.school_date_end)
        self.xtest.assertBodyTextPresent(self.school_location)


def add_test_school(xtest):
    """
    Adds a school with unique name generated as 'ЛЭШ-<number not found at the list-school page>_<random crap>'
    :param xtest: xtest instance
    :return: School instance
    """
    xtest.goto_xsm_schools()
    # determine next year
    year = 2016
    page_content = xtest.getPageContent()
    while str(year) in page_content:
        year += 1
    logging.info("Found year that is not present on this page: %s", year)
    xtest.goto_xsm_add_school()

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
    school.id = xtest.m_driver.current_url.split("=")[-1]
    return school


def get_school_id_from_selector(xtest, school_title):
    school_selector_options = xtest.get_selector_options("view-school-selector")
    for option in school_selector_options:
        if option[1] == school_title:
            return option[0]
    return None


def add_named_school(xtest, school_title):
    """
    Checks if there exists school with school_title name, if not, creates new.
    :param xtest:
        xtest instance
    :param school_title:
        string: school name
    :return:
        School instance
    """
    xtest.goto_xsm_schools()
    page_content = xtest.getPageContent()
    if school_title in page_content:
        logging.info("Found school with name: %s", school_title)
        school = School(xtest)
        school.school_title = school_title
        school.id = get_school_id(xtest, school_title)
        view_school(xtest, school)
        return get_school_information(xtest, school)

    year = 2016
    page_content = xtest.getPageContent()
    while str(year) in page_content:
        year += 1
    logging.info("Found year that is not present on this page: %s", year)
    xtest.goto_xsm_add_school()
    school = School(xtest)
    school.input(
        school_title=school_title,
        school_date_start=str(year) + ".07.15",
        school_date_end=str(year) + ".08.15",
        school_location=u"Деревня Гадюкино",
        random=False,
    )
    school.back_to_school_view()
    # FIXME(mvel): global context fix ;)
    xtest.m_conf.set_test_school_name(school.school_title)
    # FIXME(mvel): complete trash here
    school.id = xtest.m_driver.current_url.split("=")[-1]
    return school


def get_school_information(xtest, school):
    """
    Filles the school instance with information from its view
    :param xtest:
        xtest instance
    :param school:
        School instance to delete
        Only school id variable is used and must be correctly filled
    :return: school instance
    """
    view_school(xtest, school)
    school.school_title = (
        xtest.getPageContent().split('<td class="ankListRowTitle">')[1].split("</b>")[0].split("<b>")[1]
    )
    page_content = xtest.getPageContent().split('/span></td></tr>')[1].split("</table>")[0].split("</span>")[1:]
    school.school_date_start = page_content[0].split("</td></tr>")[0]
    school.school_date_end = page_content[1].split("</td></tr>")[0]
    school.school_location = page_content[2].split("</td></tr>")[0]
    school.year = school.school_date_start[0:4]
    return school


def view_school(xtest, school):
    """
        Goes to view-school for provided school.
        Only school id variable is used and must be correctly filled
        :param xtest: instance of xtet framework
        :param school: school instance to delete
        :return: school instance
    """
    xtest.gotoUrl("xsm/view-school&school_id=" + str(school.id))
    return school


def get_school_id(xtest, school_title):
    """
    Parces list-school page to find the id of a school with provided title
    :param xtest:
        xtest instance
    :param school_title:
        string: School title
    :return:
        integer: school id
    """
    xtest.goto_xsm_schools()
    page_content = xtest.getPageContent().split("<tr>")
    index = 0
    while index < len(page_content) and not (school_title in page_content[index]):
        index += 1
    # magical parsing for school id
    return int(">".join(page_content[index].split("<")).split(">")[2])


def remove_school(xtest, school):
    """
    Removes provided school instance
    Finishes work on xsm/list_school
    :param xtest: instance of xtet framework
    :param school: school instance to delete
    :return: school instance
    """
    xtest.goto_school_view(school)
    xtest.gotoUrlByLinkText(u"Правка")
    xtest.clickElementById("delete-school-submit")
    xtest.clickElementById("confirm-delete-school-submit")
    xtest.goto_xsm_schools()
    return school


class Manager(xc.XcmsTest):
    # FIXME(mvel) inheritance

    def add_course_to_teacher(self, teacher):
        self.gotoUrlByLinkText(u"Добавить курс")
        course = Course(self)
        course.input(
            course_title=u"Курс",
            course_comment=u"Какой-то комментарий",
            course_desc=u"Описание курса",
            target_class=u"7-11",
            random=True,
        )
        # XSM BUG: we should return to teacher page, not to course page!
        self.gotoUrlByLinkText(u"Вернуться к просмотру")  # view of what? Course? no, teacher!
        course.course_id = int(self.getElementValueByName("course_id"))
        self.gotoUrlByLinkText(teacher.short_alias())
        return course

    def get_current_person_id(self):
        cur_url = self.curUrl()
        m = re.search("person_id=(\d+)", cur_url)
        if m and m.groups() >= 1:
            return str(m.group(1))
        return None

    # Navigation
    def goto_anketa(self):
        self.gotoUrlByLinkText(u"Анкета")

    def goto_xsm_add_person(self):
        self.gotoUrlByLinkText(u"Добавить участника")

    def goto_xsm_anketas(self):
        self.gotoUrlByLinkText(self.getAnketaListMenuName())

    def goto_xsm(self):
        self.gotoPage("/xsm")

    def goto_xsm_schools(self):
        self.gotoUrlByLinkText(u"Школы")

    def goto_xsm_all_people(self):
        self.logAdd("goto_xsm_all_people: going to 'All People' menu. ")
        self.gotoUrlByLinkText(u"Все люди")

    def goto_xsm_active(self):
        self.logAdd("goto_xsm_active: going to 'Active' menu. ")
        self.gotoUrlByLinkText(u"Актив")

    def goto_xsm_add_school(self):
        self.logAdd("gotoAddSchool: navigating to 'Add School link (button). ")
        self.gotoUrlByLinkText(u"Добавить школу")

    def goto_xsm_courses(self):
        self.logAdd("gotoCourses: going to 'Courses' menu. ")
        self.gotoUrlByLinkText(u"Курсы")

    def goto_xsm_add_course(self):
        self.logAdd("gotoAddCourses: navigating to 'Add Course' link (button). ")
        self.gotoUrlByLinkText(u"Добавить курс")

    def goto_back_to_anketa_view(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру участника")

    def goto_back_to_person_view(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру участника")

    def goto_back_to_school_view(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру")

    def goto_back_to_course_view(self):
        self.gotoUrlByLinkText(u"Вернуться к просмотру")

    def goto_xsm_change_person_status(self):
        self.gotoUrlByLinkText(u"Сменить статус")

    def goto_school_view(xtest, school):
        """
            Goes to view-school for provided school
            :param xtest: instance of xtet framework
            :param school: school instance to delete
            :return: school instance
        """
        xtest.gotoUrl("xsm/view-school&school_id=" + str(school.id))
        return school

    @staticmethod
    def get_anketa_success_submit_message():
        return u"Поздравляем"

    @staticmethod
    def get_anketa_duplicate_submit_message():
        return u"А мы вас знаем!"
