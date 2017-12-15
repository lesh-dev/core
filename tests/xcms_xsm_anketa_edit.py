#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmAnketaEdit(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks anketa edit functional and following person processing steps.
    Steps:
    * navigate to anketa form
    * fill anketa with correct values
    * submit form
    * login as admin (root)
    * navigate to anketa list
    * clicks on new anketa
    * checks if entered data match screen form.
    * edits anketa and check that status is left intact
    """

    def run(self):
        self.ensure_logged_off()
        # anketa fill/edit positive test:
        # fields are filled with correct values.
        self.gotoRoot()
        self.goto_anketa()

        person = xsm.Person(self)
        person.input(
            last_name=u"Анкеткин",
            first_name=u"Егор",
            patronymic=u"Петрович",
            birth_date=random_crap.date(),
            school=u"Какая-то школа №" + random_crap.randomDigits(4),
            school_city=u"Магадан-" + random_crap.random_text(5),
            ank_class=random_crap.randomDigits(1) + u" В",
            phone=random_crap.phone(),
            cellular=random_crap.phone(),
            email=random_crap.email(),
            control_question=u"ампер",
            ank_mode=True,
            random=True,
        )
        # we will be warned about unfilled fields
        self.assertBodyTextPresent(u"ещё раз")
        self.clickElementById("submit_anketa-submit")
        self.assertBodyTextPresent(self.get_anketa_success_submit_message())

        self.anketa_drilldown(person)

        # just check text is on the page.
        print "Checking that filled fields are displayed on the page. "

        self.checkPersonAliasInPersonView(person.full_alias())

        self.assertBodyTextPresent(person.birth_date)
        self.assertBodyTextPresent(person.school)
        self.assertBodyTextPresent(person.school_city)
        self.assertBodyTextPresent(person.ank_class)
        self.assertBodyTextPresent(person.phone)
        self.assertBodyTextPresent(person.cellular)
        self.assertBodyTextPresent(person.email)

        # now, let's edit anketa.
        self.gotoEditPerson()

        # first, check that values in opened form match entered in anketa.
        self.assertElementValueById("last_name-input", person.last_name)
        self.assertElementValueById("first_name-input", person.first_name)
        self.assertElementValueById("patronymic-input", person.patronymic)
        self.assertElementValueById("birth_date-input", person.birth_date)
        self.assertElementValueById("school-input", person.school)
        self.assertElementValueById("school_city-input", person.school_city)
        self.assertElementValueById("ank_class-input", person.ank_class)
        # current_class should now be equal to ank_class (fresh anketa)
        self.assertElementValueById("current_class-input", person.ank_class)
        self.assertElementValueById("phone-input", person.phone)
        self.assertElementValueById("cellular-input", person.cellular)
        self.assertElementValueById("email-input", person.email)

        self.assertElementValueById("anketa_status-selector", "new")
        # change anketa field and save it.
        person.input(
            skype=random_crap.random_text(8),
        )
        self.assertBodyTextPresent(u"Участник успешно сохранён")
        self.goto_back_to_anketa_view()

        # check bug
        self.assertElementTextById("anketa_status-span", u"Новый")

        self.anketa_drilldown(person, do_login=False)
