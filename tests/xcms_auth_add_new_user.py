#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, xtest_common, random_crap, time
from xtest_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthAddNewUser(SeleniumTest):
	"""
	This test checks user add functional.
	It does following steps:
	* login as root user
	* navigate to user control panes
	* add random user
	* login as new user 
	* change user password
	* logout
	* login with incorrect password
	* change password
	* login again with changed password 
	"""
			
	def run(self):
#		self.drv().getEval("window.resizeTo(X, Y); window.moveTo(0,0);")
		self.setAutoPhpErrorChecking(True)
		
		xtest_common.assertNoInstallerPage(self)
		
		conf = XcmsTestConfig()
		
		# first, login as admin
		inpLogin = "an_test_user_" + random_crap.randomText(8)
		inpEMail = random_crap.randomEmail()
		inpPass = random_crap.randomText(10)
		inpName = u"Вася Пупкин" + random_crap.randomText(6)

		inpLogin, inpEMail, inpPass, inpName = xtest_common.createNewUser(self, conf, inpLogin, inpEMail, inpPass, inpName)
		
		print "logging as created user. "
		if not xtest_common.performLogin(self, inpLogin, inpPass):
			raise selenium_test.TestError("Cannot login as newly created user. ")
		
		# logout self 
		self.gotoUrlByLinkText("Выход")

		# test wrong auth
		print "logging as created user with incorrect password "
		if xtest_common.performLogin(self, inpLogin, "wrong_pass" + inpPass):
			raise selenium_test.TestError("I'm able to login with incorrect password. Auth is broken. ")
		
#		self.assertBodyTextPresent(u"Пароль всё ещё неверный"); already checked inside

# and now, test bug with remaining cookies:
		# we navigate to root page, and see auth panel!
		print "logging again as created user. "
		if not xtest_common.performLogin(self, inpLogin, inpPass):
			raise selenium_test.TestError("Cannot login again as newly created user. ")

		self.gotoUrlByLinkText(u"Админка")
		
		# let's try to change password.
		self.gotoUrlByLinkText(u"Сменить пароль")
		
		newPass = inpPass + "_new"
		newPass1 = self.fillElementByName("pass1", newPass)
		newPass2 = self.fillElementByName("pass2", newPass)
		if newPass1 != newPass2:
			raise RuntimeError("Unpredicted imput behavior on password change")
		newPass = newPass1
		self.clickElementByName("chpass_me")
		self.assertBodyTextPresent(u"Пароль успешно изменен.")
		self.gotoUrlByLinkText(u"Выйти")
		
		print "logging again as created user with new password"
		if not xtest_common.performLogin(self, inpLogin, newPass):
			raise selenium_test.TestError("Cannot login again as newly created user with changed password. ")

		# logout self 
		self.gotoUrlByLinkText("Выход")
		

