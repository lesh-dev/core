#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsUnitTests(xtest_common.XcmsTest):
	"""
	This test runs unittests and checks if all are passed OK.
	"""
	def run(self):

		xtest_common.assertNoInstallerPage(self)

		self.gotoPage("/unittest.php")
		self.assertSourceTextPresent(u"UNIT TESTS PASSED OK");
		
    