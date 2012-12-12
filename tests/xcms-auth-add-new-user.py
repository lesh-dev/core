#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap, time
from xcms_test_config import XcmsTestConfig
from selenium_test import SeleniumTest

class XcmsAuthAddNewUser(SeleniumTest):
	"""
	This test checks user add functional.
	It does following steps:
	1) login as root user
	2) navigate to user control panes
	3) add random user
	4) login as new user 
	"""
			
	def run(self):
#		self.drv().getEval("window.resizeTo(X, Y); window.moveTo(0,0);")
		self.setAutoPhpErrorChecking(True)
		
		conf = XcmsTestConfig()
		
	# first, login as admin
		print "logging as admin"
		tests_common.performLoginAsAdmin(self, conf.getAdminLogin(), conf.getAdminPass())
		
		print "go to user creation panel"
		
		#	self.gotoRoot()
		self.gotoUrlByLinkText(u"Админка")
		# navigate to users CP
		print "goto user list."
		self.gotoUrlByLinkText(u"Пользователи")
		self.assertBodyTextPresent(u"Администрирование пользователей")
		self.gotoUrlByLinkText(["Create user", u"Создать пользователя"])
		
		inpLogin = "an_test_user_" + random_crap.randomText(8)
		inpEMail = random_crap.randomEmail()
		inpPass = random_crap.randomText(10)
		inpName = u"Вася Пупкин" + random_crap.randomText(6)
		#inpName = u"Вася Пупкин" + selenium_test.randomText(6)
		
		#<tr><td colspan="2"><b>Учетные данные</b>                               </td></tr>
		#<tr><td>Имя пользователя:   </td><td> <input name="login">                </td></tr>
		#<tr><td>Пароль:             </td><td> <input type="password" name="p1">   </td></tr>
		#<tr><td>Пароль  (еще раз):  </td><td> <input type="password" name="p2">   </td></tr>
		#<tr><td>Настоящее имя:      </td><td> <input name="name">                 </td></tr>
		#<tr><td>Электропочта:       </td><td> <input name="email">                </td></tr>
		#<tr><td colspan="2">  <input type="checkbox" name="notify_user" />	
		inpLogin = self.fillElementById("login", inpLogin)
		print "login = '" + inpLogin + "'"
		if inpLogin == "":
			raise RuntimeError("Filled login value is empty!")
		
		inpEMail = self.fillElementById("email", inpEMail)
		inpPass1 = self.fillElementById("password", inpPass)
		print "original pass: " + inpPass
		inpPass2 = self.fillElementById("password_confirm", inpPass)
		if inpPass1 != inpPass2:
			raise RuntimeError("Unpredicted input behavior")
		inpPass = inpPass1
		print "actual pass: " + inpPass
		
		inpName = self.fillElementById("name", inpName)
		
		# set notify checkbox.
		self.clickElementByName("notify_user")
		# send form
		
		self.clickElementByName("create_user")
		
		print "user created, going to user list again to refresh. "
		
		time.sleep(2)
		# here is a usability issue: user not appears in the list.
		# refresh user list
		self.gotoUrlByLinkText(u"Пользователи")
		
		self.gotoUrlByLinkText(inpLogin)
		
		self.assertTextPresent("//div[@class='user-ops']", inpLogin)
		
		#logoff root
		tests_common.performLogout(self)
		
		print "logging as created user. "
		if not tests_common.performLogin(self, inpLogin, inpPass):
			raise selenium_test.TestError("Cannot login as newly created user. ")
		
		# logout self 
		self.gotoUrlByLinkText("Выход")

		# test wrong auth
		print "logging as created user with incorrect password "
		if tests_common.performLogin(self, inpLogin, "wrong_pass" + inpPass):
			raise selenium_test.TestError("I'm able to login with incorrect password. Auth is broken. ")
		
#		self.assertBodyTextPresent(u"Пароль всё ещё неверный"); already checked inside

# and now, test bug with remaining cookies:
		# we navigate to root page, and see auth panel!
		print "logging again as created user. "
		if not tests_common.performLogin(self, inpLogin, inpPass):
			raise selenium_test.TestError("Cannot login again as newly created user. ")

		# logout self 
#		self.gotoUrlByLinkText("Выход")
		
	
# def main():
selenium_test.RunTest(XcmsAuthAddNewUser())

