#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium_test import SeleniumTest


class SelfTest(SeleniumTest):
    """
    This test checks SeleniumTest class.
    """

    def run(self):
        self.setAutoPhpErrorChecking(True)
        self.goto_root()

        # conf = XcmsTestConfig()

        # TODO: somthing is outdated here
        # xtest_common.perform_login_as_admin(self, conf.getAdminLogin(), conf.getAdminPass())

        self.gotoUrlByLinkText(u"Анкеты")
        self.gotoUrlByLinkText(u"TESTЧаПаевa855d Василийb02")

        self.gotoUrlByLinkText(u"Редактировать анкетные данные")
        ele = self.getElementById("anketa_status-selector")
        #print dir(ele)
        optList = ele.find_elements_by_xpath(u"//option[@value='progress']")
        # print opt.text
        for i in optList:
            print "text: '" + i.text + "'"

        #self.setOptionValueByIdAndValue("anketa_status-selector", "progress")
