#!/usr/bin/python
# -*- coding: utf8 -*-

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
    * check person's status and autocomments
    """

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()

        self.gotoXsm()
        self.gotoXsmActive()
        self.gotoXsmAddPerson()

        # generate
        inpLastName = u"Статусов" + random_crap.randomText(4)
        inpFirstName = u"Иннокентий_" + random_crap.randomText(3)
        inpMidName = u"Петрович_" + random_crap.randomText(3)

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)

        self.clickElementById("update-person-submit")

        self.gotoBackToPersonView()

        fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
        # check if person alias is present (person saved correctly)

        self.checkPersonAliasInPersonView(fullAlias)

        self.assertElementTextById("anketa_status-span", u"Активный")

        self.gotoXsmChangePersonStatus()

        self.setOptionValueByIdAndValue("anketa_status-selector", "discuss")
        commentText = u"Комментарий к смене статуса " + random_crap.randomCrap(5)
        commentText = self.fillElementById("comment_text-text", commentText)

        self.clickElementById("update-person_comment-submit")
        self.gotoBackToPersonView()

        self.assertBodyTextPresent(u"Статус Активный изменён на Обсуждается")
        self.assertBodyTextPresent(commentText)
