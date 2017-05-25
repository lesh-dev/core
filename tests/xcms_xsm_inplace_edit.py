#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common
import random_crap


class XcmsXsmInplaceEdit(xsm.Manager, xtest_common.XcmsTest):
    """
    #979
    Creating a new particiant with some forest status, changing his status, checking changes took place
    """

    fio_filter_id = "show_name_filter-input"

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoUrlByLinkText(u"Выходы в лес")

        # create new person
        self.clickElementById("clear_forest-submit")
        self.gotoUrlByLinkText(u"Добавить участника")
        self.setOptionValueByIdAndValue("anketa_status-selector", "less")
        inp_first_name = u"Ричард" + random_crap.random_text(6)
        inp_last_name = u"Фейнман" + random_crap.random_text(6)

        inp_first_name = self.fillElementByName("first_name", inp_first_name)
        inp_last_name = self.fillElementByName("last_name", inp_last_name)

        self.setOptionValueByIdAndValue("forest_1-selector", "maybe")
        self.clickElementById("update-person-submit")
        self.assertBodyTextPresent(u"Участник успешно сохранён")

        self.gotoUrlByLinkText(u"Лес")
        self.fillElementById(self.fio_filter_id, inp_last_name)
        self.clickElementByName("show-person")

        self.assertBodyTextPresent(u"ХЗ")

        self.doubeClickElementById("p1-forest_1-span")
        self.setOptionValueByIdAndValue("forest_1-selector", "no")

        self.assertBodyTextPresent(u"Не идёт")
        self.assertBodyTextNotPresent(u"ХЗ")
