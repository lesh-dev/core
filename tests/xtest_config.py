#!/usr/bin/python
# -*- coding: utf8 -*-

class XcmsTestConfig:
	def __init__(self):
		self.m_adminLogin = "root"
		self.m_adminPass = "root"
		self.m_testAnketaSend = True
		
	def getAdminLogin(self):
		return self.m_adminLogin;

	def getAdminPass(self):
		return self.m_adminPass;

	def getAnketaNamePrefix(self):
		if self.m_testAnketaSend:
			return "TEST"
		else:
			return "NO-MAIL-TEST"
				
	