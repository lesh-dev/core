#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import os


class XcmsContestSubmitWork(xtest_common.XcmsTest):
    """
    This test checks contest work uploading.
    Steps:
    * login as ??? (now as admin, but contest manager should be there)
    * goto contest management page
    * add new work
    * check if it was really loaded
    """

    def run(self):
        self.ensure_logged_off()
        # TODO(mvel): Add contest manager role
        self.performLoginAsAdmin()
        self.gotoPage("/ctx")

        self.gotoUrlByLinkText(u"Добавить работу")

        inp_fio = u"Участник_Олимпиады_" + random_crap.random_text(6)
        inp_email = random_crap.randomEmail()
        inp_comment = random_crap.random_text(6)

        work_file = os.getcwd() + "/contest-work-sample.png"
        inp_fio = self.fillElementByName("name", inp_fio)
        _ = self.fillElementByName("mail", inp_email)
        _ = self.fillElementByName("work", work_file, clear=False)
        # WTF??? Why 'status', not 'comment'?
        _ = self.fillElementByName("status", inp_comment)
        self.clickElementByName("ctx_add_or_edit_form_contestants_x")

        # check that work appears in the list
        self.gotoUrlByLinkText(u"Работы")
        self.assertBodyTextPresent(inp_fio)
