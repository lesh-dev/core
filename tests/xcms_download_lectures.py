#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsDownloadLectures(xtest_common.XcmsTest):
    """
    This test checks /lectures folder (check it is not confused by rewrite rules)
    It does following steps:
    * navigates to /lectures folder;
    * downloads some files from this folder.
    """
    def run(self):
        self.gotoPage("/")
        self.gotoPage("/lectures")
        self.gotoPage("/lectures/iext.pdf")
        self.gotoPage("/lectures/iext-by-an.pdf")
        self.gotoPage("/lectures/prak")
