#!/usr/bin/python
# -*- coding: utf8 -*-

class XcmsTestConfig:
    def __init__(self):
        self.m_adminLogin = "root"
        self.m_adminPass = "root"
        self.m_notifyEmail = "vdm-photo@ya.ru"
        self.m_testAnketaSend = True
        self.m_phpErrorCheckFlag = False #TODO: change!
        
    def getAdminLogin(self):
        return self.m_adminLogin

    def getAdminPass(self):
        return self.m_adminPass

    def getNotifyEmail(self):
        return self.m_notifyEmail

    def getPhpErrorCheckFlag(self):
        return self.m_phpErrorCheckFlag

    def getAnketaNamePrefix(self):
        if self.m_testAnketaSend:
            return "TEST"
        else:
            return "NO-MAIL-TEST"
                
    