# -*- coding: utf8 -*-

import xsm
import xtest_common
import random


_SCHOOL_NAME = "add_person_to_school_test"


class XcmsXsmAddPersonToSchool(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks a new person can be added to a new school.
    Steps:
    * login as root
    * create/use existing "add_person_to_school_test" school
    * navigate to add member form
    * fill form with correct and new values
    * submit form
    * check whether form is submitted correctly
    * navigate to add member form
    * fill form with same first and last names
    * submit form
    * check whether duplicate check strikes or not
    * delete the relation record between the school and the student
    * navigate to add member form
    * fill form with same first and last names
    * submit form
    * checks whether it is advised to add an existing student
    """

    def run(self):
        """
        Look for the class documentation
        :return: None
        """
        self.ensure_logged_off()
        self.performLoginAsManager()
        self.goto_xsm()

        # obtain fresh member
        self.goto_xsm_all_people()
        person_unique = 0
        base_name = u"Анкеткин_"
        page_content = self.getPageContent()
        while base_name + str(person_unique) in page_content:
            person_unique += 1

        self.goto_xsm_schools()
        school = xsm.add_named_school(self, _SCHOOL_NAME)
        school_id = xsm.get_school_id(self, _SCHOOL_NAME)
        self.gotoUrlByLinkText(u"Участники школ")
        if not self.get_url_by_link_data(school.school_title, fail=False):
            # school is hidden in school selector
            self.setOptionValueByIdAndValue("view-school-selector", school_id)

        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person = xsm.Person(self)
        last_name = base_name + str(person_unique)
        first_name = u"Егор"
        person.input(
            last_name=last_name,
            first_name=first_name,
            patronymic=u"Петрович",
            birth_date=u"11.11.1111",
            school=u"Какая-то школа №0000",
            school_city=u"Магадан-23",
            ank_class=u"15 В",
            phone=u"8800" + str(random.randint(100000, 899999)),
            cellular=u"8800" + str(random.randint(100000, 899999)),
            email=u"spaminatro" + str(random.randint(10000, 89999)) + "@10minutemail.com",
            ank_mode=False,
        )
        self.assertBodyTextPresent(u"Участник успешно сохранён")
        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person.input(
            last_name=last_name,
            first_name=first_name,
            ank_mode=False,
            expect=person.EXP_DUPLICATE,
        )
        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(person.last_name + u" " + person.first_name)
        self.gotoUrlByLinkTitle(u"Отчислить с " + school.school_title)
        self.clickElementById("confirm-delete-person_school-submit")
        self.gotoUrlByLinkText(u"Участники школ")
        if not self.get_url_by_link_data(school.school_title, fail=False):
            # school is hidden in school selector
            self.setOptionValueByIdAndValue("view-school-selector", school_id)

        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person.input(
            last_name=last_name,
            first_name=first_name,
            ank_mode=False,
            expect=person.EXP_NOT_AT_SCHOOL,
        )
        self.clickElementById("update-person-submit")
        self.assertBodyTextPresent(u"Участник успешно сохранён")
