#!/usr/bin/python
# -*- coding: utf8 -*-

class XcmsTestConfig:
    def __init__(self):
        self.m_adminLogin = "root"
        self.m_adminPass = "root"
        self.m_notifyEmail = "vdm-photo@ya.ru"
        self.m_testAnketaSend = True
        self.m_phpErrorCheckFlag = True
        
    def getAdminLogin(self):
        return self.m_adminLogin

    def getAdminPass(self):
        return self.m_adminPass

    def getNotifyEmail(self):
        return self.m_notifyEmail

    def getPhpErrorCheckFlag(self):
        return self.m_phpErrorCheckFlag

    def getAnketaNamePrefix(self):
        return ""
        #if self.m_testAnketaSend:
            #return "TEST"
        #else:
            #return "NO-MAIL-TEST"
    def getForgottenPasswordCaptcha(self):
        return u"ампер"
    
    def getValidEmail1(self):
        return "testsite001@fizlesh.ru"
    
    def getValidEmail2(self):
        return "testsite002@fizlesh.ru"
    
    def getTestSchoolName(self):
        return u"ЛЭШ-2013"
                
    