#!/usr/bin/python
# -*- coding: utf8 -*-


class XcmsTestConfig:
    def __init__(self):
        self._admin_login = "root"
        self._admin_password = "HCYHL7JXG4QG"

        self._manager_login = "root"
        self._manager_password = "HCYHL7JXG4QG"

        self.m_notifyEmail = "vdm-photo@ya.ru"
        self.m_phpErrorCheckFlag = True
        self.school_name = u"ЛЭШ-2013"

    def get_admin_login(self):
        return self._admin_login

    def get_admin_password(self):
        return self._admin_password

    def get_manager_login(self):
        return self._manager_login

    def get_manager_password(self):
        return self._manager_password

    def getNotifyEmail(self):
        return self.m_notifyEmail

    def getPhpErrorCheckFlag(self):
        return self.m_phpErrorCheckFlag

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
        return self.school_name

    def set_test_school_name(self, school_name):
        self.school_name = school_name
