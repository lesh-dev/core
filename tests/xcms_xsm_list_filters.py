#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap

class XcmsXsmListFilters(xtest_common.XcmsTest):
    """
    This test checks various filters in XSM lists.
    """
    def run(self):
        self.performLoginAsManager()
        self.gotoRoot()
        self.gotoXsm()
        self.gotoAllPeople()
        
        # one line expected
        self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        shortAlias = u"Вельтищев Михаил"
        alias = shortAlias + u" Николаевич"
        self.fillElementByName("show_name_filter", alias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(shortAlias) != 1:
            self.failTest("Found more than one anketa with exact FIO. Filters are broken. ")

        # two lines expected
        #self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        shortAliases = [u"Вельтищев Михаил", u"Вельтищев Дмитрий"]
        alias = u"Вельтищев"
        self.fillElementByName("show_name_filter", alias)
        
        self.clickElementByName("show-person")
        
        for alias in shortAliases:
            if self.countIndexedUrlsByLinkText(alias) != 1:
                self.failTest("Expected link {0} not found. Filters are broken. ".format(alias))
            
        # none lines expected
        #self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        alias = "qwerty"
        alias = self.fillElementByName("show_name_filter", alias)
        self.clickElementByName("show-person")
        if self.countIndexedUrlsByLinkText(alias) != 0:
            self.failTest("This search should not return anything. Filters are broken. ")

        # none lines expected
        #self.setOptionValueByIdAndValue("show_anketa_status-selector", "all")
        alias = u"Демарин Дмитрий"
        self.fillElementByName("show_name_filter", alias)
        self.sendEnterByName("show_name_filter")
        if self.countIndexedUrlsByLinkText(alias) != 1:
            self.failTest("This search should return one recored. Filters are broken. ")
