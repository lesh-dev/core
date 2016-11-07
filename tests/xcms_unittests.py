#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common

class XcmsUnitTests(xtest_common.XcmsBaseTest):
    """
    This test runs unittests and checks if all are passed OK.
    """
    def run(self):

        self.assert_no_installer_page()

        self.gotoPage("/unittest.php")
        self.assertSourceTextPresent(u"UNIT TESTS PASSED OK");
        
    def check_doc_type(self):
        self.logAdd("DOCTYPE check is disabled for Unit-tests page. ", "warning")
