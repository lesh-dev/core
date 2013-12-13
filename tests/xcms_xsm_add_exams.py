#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common, random_crap
from xtest_config import XcmsTestConfig

class XcmsXsmAddExams(xtest_common.XcmsTest):
    """
    This test checks exam add functional.
    It does following:
    * login as admin
    * enter 'all people list'
    * add new person
    * add person to some school
    * add some courses
    * set exam status
    """

    def addExamsById(self, examIdList):
        for exam in examIdList:
            self.addExamById(exam)
    
    def addExamById(self, exam):
        self.gotoUrlByLinkText(u"Добавить зачёт")

        self.setOptionValueByIdAndValue("course_id-selector", exam)
        self.clickElementByName("update-exam")
        xtest_common.gotoBackToPersonView(self)
        
    def setExamPassed(self, examLineList):
        for examLine in examLineList:            
            self.gotoIndexedUrlByLinkText(u"Прослушан", examLine)
            self.setOptionValueByIdAndValue("exam_status-selector", "passed")
            
            examComment = u"Коммент к зачёту: " + random_crap.randomText(4)
            self.fillElementByName("exam_comment", examComment)
            self.clickElementByName("update-exam")
            xtest_common.gotoBackToPersonView(self)
            
        self.assertBodyTextPresent(u"Сдан")
            

    def setExamNotPassed(self, examLineList):
        for examLine in examLineList:            
            self.gotoIndexedUrlByLinkText(u"Прослушан", examLine)
            self.setOptionValueByIdAndValue("exam_status-selector", "notpassed")
            
            examComment = u"Коммент к зачёту: " + random_crap.randomText(4)
            self.fillElementByName("exam_comment", examComment)
            self.clickElementByName("update-exam")
            xtest_common.gotoBackToPersonView(self)
            
        self.assertBodyTextPresent(u"Не сдан")


    def run(self):
        conf = XcmsTestConfig()
        self.setAutoPhpErrorChecking(conf.getPhpErrorCheckFlag())
        xtest_common.assertNoInstallerPage(self)

        testMailPrefix = conf.getAnketaNamePrefix()

        adminLogin = conf.getAdminLogin()
        adminPass = conf.getAdminPass()

        xtest_common.setTestNotifications(self, conf.getNotifyEmail(), adminLogin, adminPass)
        xtest_common.performLoginAsAdmin(self, adminLogin, adminPass)

        xtest_common.gotoAllPeople(self)

        self.gotoUrlByLinkText(u"Добавить участника")

        # generate
        inpLastName = testMailPrefix + u"Зачётов" + random_crap.randomText(5);
        inpFirstName = u"Андрей_" + random_crap.randomText(3)
        inpMidName = u"Михалыч_" + random_crap.randomText(3)

        inpLastName = self.fillElementById("last_name-input", inpLastName)
        inpFirstName = self.fillElementById("first_name-input", inpFirstName)
        inpMidName = self.fillElementById("patronymic-input", inpMidName)
        
        # set student flag
        self.clickElementById("is_student-checkbox")
        
        self.clickElementById("update-person-submit")
        
        xtest_common.gotoBackToPersonView(self)

        fullAlias = inpLastName + " " + inpFirstName + " " + inpMidName
        # check if person alias is present (person saved correctly)
        xtest_common.checkPersonAliasInPersonView(self, fullAlias)
        
        self.gotoUrlByLinkText(u"ЛЭШ-2013")
        self.assertBodyTextPresent(u"На данной школе не присутствовал")
        self.gotoUrlByLinkText(u"Зачислить")
        self.clickElementByName("update-person_school")
        xtest_common.gotoBackToPersonView(self)

        #<option  value="95">Базовое электричество &#8212; Тараненко Сергей</option>
        #<option  value="134">Биомеханика &#8212; Преподаватель Другого</option>
        #<option  value="83">Ботаника &#8212; Преподаватель Другого</option>
        #<option  value="73">Введение в технику эксперимента &#8212; Пюрьбеева Евгения</option>
        #<option  value="119">Введение в химию &#8212; Марьясина Софья</option>
        #<option  value="101">Видеосъёмка &#8212; Дюно-Люповецкий Влас</option>
        #<option  value="137">Генетические алгоритмы &#8212; Мироненко-Маренков Антон</option>
        #<option  value="91">Геометрическая оптика &#8212; Пилипюк Дарья</option>        

        self.assertBodyTextPresent(u"Зачёты")
        
        self.addExamsById([95, 119, 91, 134, 73, 107, 130, 133])
        
        self.setExamPassed([1, 3, 5])
        self.setExamNotPassed([1, 2, 4])
                
        
        
        

