# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmAddPersonToSchool(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks a new person can be added to a new school.
    Steps:
    * login as root
    * create or uses existing "add_person_to_school_test" school
    * navigate to add member form
    * fill form with correct and new values 
    * submit form
    * check if form is submitted correctly
    * navigate to add member form
    * fill form with same first and last names
    * submit form
    * check if duplicate block worked
    * delete the relation record between the school and the student
    * navigate to add member form
    * fill form with same first and last names
    * submit form
    * checks if advised to add an existing student
    """

    def run(self):
        """
        Look for the class documentation
        :return: None 
        """
        self.ensure_logged_off()
        self.performLoginAsManager()
        self.goto_xsm()
        self.goto_xsm_schools()
        school = xsm.add_named_school(self, "add_person_to_school_test")
        self.gotoUrlByLinkText(u"Участники школ")
        self.gotoUrlByLinkText(school.school_title)
        person_unique = 0
        page_content = self.getPageContent()
        while str(person_unique) in page_content:
            person_unique += 1
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person = xsm.Person(self)
        last_name = u"Анкеткин_" + str(person_unique)
        first_name  = u"Егор"
        person.input(
            last_name=last_name,
            first_name=first_name,
            patronymic=u"Петрович",
            birth_date=u"11.11.1111",
            school=u"Какая-то школа №0000",
            school_city=u"Магадан-23",
            ank_class=u"15 В",
            phone=u"88005553535",
            cellular=u"88005553535",
            email=u"spaminatro228@10minutemail.com",
            ank_mode=False,
        )
        self.assertBodyTextPresent(u"Участник успешно сохранён")
        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person.input(
            last_name=last_name,
            first_name=first_name,
            ank_mode=False,
        )
        self.assertBodyTextPresent(u"Люди с такими именем и фамилией уже зачислены на эту школу")
        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(person.last_name + u" " + person.first_name)
        self.gotoUrlByLinkTitle(u"Отчислить с " + school.school_title)
        self.clickElementById("confirm-delete-person_school-submit")
        self.gotoUrlByLinkText(u"Участники школ")
        self.gotoUrlByLinkText(school.school_title)
        self.gotoUrlByLinkText(u"Добавить нового участника")
        person.input(
            last_name=last_name,
            first_name=first_name,
            ank_mode=False,
        )
        self.assertBodyTextPresent(u"Люди с такими именем и фамилией уже есть в базе и не зачислены на школу. Проверьте, возможно вы хотели добавить одного из этих людей:")
        self.clickElementById("update-person-submit")
        self.assertBodyTextPresent(u"Участник успешно сохранён")

