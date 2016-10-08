#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap


class XcmsXsmClearForestStatus(xtest_common.XcmsTest):

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoUrlByLinkText(u"Выходы в лес")

        # create new person
        self.gotoUrlByLinkText(u"Добавить участника")
        self.setOptionValueByIdAndValue("anketa_status-selector", "less")
        inpFirstName = u"Бруно" + random_crap.randomText(6)
        inpLastName = u"Понтекорво" + random_crap.randomText(6)

        inpFirstName = self.fillElementByName("first_name", inpFirstName)
        inpLastName = self.fillElementByName("last_name", inpLastName)

        self.setOptionValueByIdAndValue("forest_1-selector", "maybe")
        self.setOptionValueByIdAndValue("forest_2-selector", "no")
        self.clickElementById("update-person-submit")
        self.assertBodyTextPresent(u"Участник успешно сохранён")

        self.gotoUrlByLinkText(u"Лес")
        self.assertBodyTextPresent(u"ХЗ")
        self.assertBodyTextPresent(u"Не идёт")

        self.clickElementById("clear_forest-submit")
        self.assertBodyTextNotPresent(u"ХЗ")
        self.assertBodyTextNotPresent(u"Не идёт")
