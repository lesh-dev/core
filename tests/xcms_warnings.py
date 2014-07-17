#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common

class XcmsWarnTest(xtest_common.XcmsBaseTest):
    """
    This test runs unittests and checks if all are passed OK.
    """
    def run(self):

        self.assertNoInstallerPage()
        self.setAutoPhpErrorChecking(False)
        self.gotoPage("/warntest.php")
        self.assertSourceTextPresent("This page intentionally contains errors")
        checkResult, suspWord = self.checkPhpErrors()
        if not checkResult:
            self.failTest("Warnings not detected. ");
        
    def checkDocType(self):
        self.logAdd("DOCTYPE check is disabled for Warn-tests page. ", "warning")
