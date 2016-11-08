#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmPhones(xtest_common.XcmsTest):
    """
    This test checks person phone parsing feature
    It does following:
    * adds new person
    * fill some examples of valid phone specifications
    * checks if they are correctly displayed on person card.
    * checks phone automatic formatting
    """

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()

        self.gotoXsm()
        self.gotoXsmActive()
        self.goto_xsm_add_person()

        person = xsm.Person(self)
        person.input(
            last_name=u"Телефонов",
            first_name=u"Самсунг",
            patronymic=u"Нокиевич",
            random=True,
            cellular_list=["+7(900)000-00-00", "+7(900)999-99-99"],
            phone_list=["8-900-000-00-00", "+7-900-999-99-99"],
        )
        person.back_to_person_view()

        person_id = xsm.get_current_person_id(self)

        for i in range(0, 2):
            site_cellular_phone = person.get_row_value(person_id, 'cellular', i)
            site_phone = person.get_row_value(person_id, 'phone', i)
            self.assert_equal(person.cellular_list[i], site_cellular_phone, "Cell phones #{} do not match. ".format(i))
            self.assert_equal(person.phone_list[i], site_phone, "Phones #{} do not match. ".format(i))

        self.gotoEditPerson()
        person.input(
            phone="+79261112233",
            cellular="89261112233",
        )
        self.gotoBackToPersonView()

        site_cellular_phone = person.get_row_value(person_id, 'cellular', 0)
        site_phone = person.get_row_value(person_id, 'phone', 0)

        self.assert_equal(site_phone, "8(926)111-22-33", "Phone was not autoformatted. ")
        self.assert_equal(site_cellular_phone, "8(926)111-22-33", "Cellular phone was not autoformatted. ")
