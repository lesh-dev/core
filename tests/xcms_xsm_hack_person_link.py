#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common

class XcmsXsmHackPersonLink(xtest_common.XcmsTest):
    """
    This test checks person phone parsing feature
    It does following:
    * logins as xsm manager
    * navigated malformed person link
    """

    def run(self):
        self.ensure_logged_off()

        self.performLoginAsManager()

        self.goto_xsm_all_people()
        self.gotoPage("/xsm/view-person&person_id=286")
        self.gotoPage("/xsm/view-person&person_id=far_away")
        self.assertBodyTextPresent(u"Объект")
        
