#!/usr/bin/python
# -*- coding: utf8 -*-


class XcmsTestConfig:
    def __init__(self):
        self.m_adminLogin = "root"
        self.m_adminPass = "root"
        self.m_notifyEmail = "vdm-photo@ya.ru"
        self.m_testAnketaSend = True  # в настоящее время не используется
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
        """
            Артефакт старого режима тестирования анкет, в котором в имена приписывались
            слова TEST, NO-MAIL-TEST и т.п.
        """
        return ""

    def getForgottenPasswordCaptcha(self):
        return u"ампер"

    def getValidEmail(self, email_id=1):
        if email_id == 1:
            return "testsite001@fizlesh.ru"
        elif email_id == 2:
            return "testsite002@fizlesh.ru"
        elif email_id == 'mail.ru':
            return "m.velt@mail.ru"

    def getTestSchoolName(self):
        return u"ЛЭШ-2013"
