#!/usr/bin/python
# -*- coding: utf8 -*-

import xsm
import xtest_common


class XcmsXsmHackPersonLink(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks person phone parsing feature
    It does following:
    * Logs in as XSM manager
    * Navigates malformed person link
    """

    def run(self):
        self.ensure_logged_off()

        self.perform_login_as_manager()
        self.goto_xsm()
        self.goto_xsm_all_people()
        self.gotoPage("/xsm/view-person&person_id=286")
        self.gotoPage("/xsm/view-person&person_id=far_away")
        self.assertBodyTextPresent(u"Объект")
