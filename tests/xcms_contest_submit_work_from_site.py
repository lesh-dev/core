#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import logging

import xtest_common
import random_crap

M = 1000 * 1000


class XcmsContestSubmitWorkFromSite(xtest_common.XcmsTest):

    def _test_work_submit(self, file_size, need_success, fill_work=True):
        self.goto_root()

        # FIXME(mvel): if contest will be raised up, this should be fixed too
        # self.gotoUrlByLinkText(u"Олимпиада", attribute=self.CONTENT)
        self.gotoUrl("/contest")

        self.gotoUrlByLinkText(u"Отправить решение", attribute=self.CONTENT)

        work_file = os.path.join(os.getcwd(), 'contest-work-sample.png')
        if fill_work:
            # create file if necessary
            if file_size >= 0:
                with open(work_file, 'w') as f:
                    f.write('Q' * file_size)
            else:
                # negative size means no file at all
                try:
                    os.remove(work_file)
                except OSError:
                    # ignore file removal error
                    pass

            work_file = self.fillElementByName("attachment", work_file)

        logging.info("Size: %s", file_size)

        self.clickElementById("send-contest-submit")
        if need_success:
            self.assertBodyTextPresent(u"Спасибо, Ваше решение принято!")
        else:
            if file_size >= 0:
                self.assertBodyTextPresent(u"Ошибка отправки решения")

            if file_size > 16 * 1000 * 1000:
                self.assertBodyTextPresent(u"файл слишком большой")

        self.assertPhpErrors()
        # cleanup
        if os.path.exists(work_file):
            os.remove(work_file)

    def run(self):
        self.ensure_logged_off()

        logging.info("send empty form")
        self._test_work_submit(file_size=-1, need_success=False, fill_work=False)

        logging.info("send non-existent file")
        self._test_work_submit(file_size=-1, need_success=False)

        logging.info("send small file")
        self._test_work_submit(file_size=10, need_success=False)

        logging.info("send large file")
        self._test_work_submit(file_size=25 * M, need_success=False)

        # send very large file (does not work)
        # self._test_work_submit(file_size=80*1000*1000, need_success=False)

        logging.info("Finally send normal file")
        self._test_work_submit(file_size=2 * M, need_success=True)

        # Send a link
        self.gotoUrlByLinkText(u"Отправить решение", attribute=self.CONTENT)
        inp_link = u"Бла-бла-бла" + random_crap.random_text(6)
        self.fillElementByName("fileexchange", inp_link)
        self.clickElementById("send-contest-submit")

        self.assertBodyTextPresent(u"Спасибо, Ваше решение принято!")
        self.assertPhpErrors()
