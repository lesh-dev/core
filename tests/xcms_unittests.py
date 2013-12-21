#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common

class XcmsUnitTests(xtest_common.XcmsBaseTest):
	"""
	This test runs unittests and checks if all are passed OK.
	"""
	def run(self):

		self.assertNoInstallerPage()

		self.gotoPage("/unittest.php")
		self.assertSourceTextPresent(u"UNIT TESTS PASSED OK");
		
    
