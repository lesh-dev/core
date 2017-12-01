#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmClearForestStatus(xsm.Manager, xtest_common.XcmsTest):
    """
    Сначала заполняем лесные статусы, потом их чистим и проверяем,
    что они действительно очистились. Заходим непременно под Администратором.
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.goto_xsm()
        self.gotoUrlByLinkText(u"Выходы в лес")

        self.goto_xsm_add_person()
        person = xsm.Person(self)
        person.input(
            first_name=u"Бруно",
            last_name=u"Понтекорво",
            anketa_status="less",
            forest_1="maybe",
            forest_2="no",
            random=True,
        )

        self.gotoUrlByLinkText(u"Лес")
        self.assertBodyTextPresent(u"ХЗ")
        self.assertBodyTextPresent(u"Не идёт")

        self.clickElementById("clear_forest-submit")
        self.assertBodyTextNotPresent(u"ХЗ")
        self.assertBodyTextNotPresent(u"Не идёт")
