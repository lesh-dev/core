#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import os


class XcmsContestSubmitWork(xtest_common.XcmsTest):
    """
    This test checks contest work uploading.
    Steps:
    * login as ???
    * goto contest management page
    * add new work
    * check if it was really loaded
    """

    def run(self):
        self.ensure_logged_off()
        self.performLoginAsAdmin()
        self.gotoPage("/ctx")

        self.gotoUrlByLinkText(u"Добавить работу")

        inpFIO = u"Участник_Олимпиады_" + random_crap.random_text(6)
        inpEmail = random_crap.randomEmail()
        inpComment = random_crap.random_text(6)

        workFile = os.getcwd() + "/contest-work-sample.png"
        inpFIO = self.fillElementByName("name", inpFIO)
        inpEmail = self.fillElementByName("mail", inpEmail)
        workFile = self.fillElementByName("work", workFile, clear=False)
        # WTF??? Why 'status', not 'comment'?
        inpComment = self.fillElementByName("status", inpComment)
        self.clickElementByName("ctx_add_or_edit_form_contestants_x")

        # check that work appears in the list
        self.gotoUrlByLinkText(u"Работы")
        self.assertBodyTextPresent(inpFIO)
