#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmChangeStatusQuick(xtest_common.XcmsTest):
    """
    This test checks quick status change functional.
    Steps:
    * login as admin
    * enter 'all people list'
    * add new person
    * change person status
    * check person's status and auto-comments
    """

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()

        self.gotoXsm()
        self.gotoXsmActive()
        self.goto_xsm_add_person()

        person = xsm.Person(self)
        person.input(
            last_name=u"Статусов",
            first_name=u"Иннокентий",
            patronymic=u"Петрович",
            random=True,
        )
        person.back_to_person_view()

        self.assertElementTextById("anketa_status-span", u"Активный")

        self.gotoXsmChangePersonStatus()

        self.setOptionValueByIdAndValue("anketa_status-selector", "discuss")
        comment_text = u"Комментарий к смене статуса " + random_crap.randomCrap(5)
        comment_text = self.fillElementById("comment_text-text", comment_text)

        self.clickElementById("update-person_comment-submit")
        self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Статус Активный изменён на Обсуждается")
        self.assertBodyTextPresent(comment_text)
