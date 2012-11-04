#!/usr/bin/python
# -*- coding: utf8 -*-

import selenium_test, tests_common, random_crap
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
		self.gotoUrlByLinkText("Create user")
		
		
		inpLogin = "an_test_user_" + random_crap.randomText(8)
		inpEMail = random_crap.randomEmail()
		inpPass1 = random_crap.randomText(10)
		inpPass2 = inpPass1
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
		inpEMail = self.fillElementById("email", inpEMail)
		inpPass1 = self.fillElementById("password", inpPass1)
		inpPass2 = self.fillElementById("password_confirm", inpPass2)
		inpPass1 = self.fillElementById("name", inpName)
		
		# set notify checkbox.
		self.clickElementByName("notify_user")
		# send form
		
		self.clickElementByName("create_user")
		
		print "user created, going to user list again to refresh. "
		
		# here is a usability issue: user not appears in the list.
		# refresh user list
		self.gotoUrlByLinkText(u"Пользователи")
		
		self.gotoUrlByLinkText(inpLogin)
		
		self.assertBodyTextPresent(u"Известен под логином " + inpLogin)
		
		print "logging as created user. "
		tests_common.performLogin(self, inpLogin, inpPass1)	
	
# def main():
selenium_test.RunTest(XcmsAuthAddNewUser())

