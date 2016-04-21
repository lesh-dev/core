#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import os


class XcmsContestSubmitWorkFromSite(xtest_common.XcmsTest):
   

    def run(self):

        
        self.gotoUrlByLinkText(u"Заочная олимпиада")
        self.gotoUrlByLinkText(u"Отправить решение")
        
        #send empty form
        self.clickElementById("send-contest-submit")
        self.assertBodyTextPresent(u"Ошибка отправки решения")
        self.assertPhpErrors()
        
        #send unexistent file
        workFile = os.getcwd() + "/contest-work-sample-nope"
        workFile = self.fillElementByName("attachment", workFile)
        self.clickElementById("send-contest-submit")
        self.assertBodyTextPresent(u"Ошибка отправки решения")
        self.assertPhpErrors()
        
        #send small file
        with open('contest-work-sample-small', 'w') as f:
            f.write('Q' * 10)        
        #I don't understand this
        #And I don't know how to delete qqq
        workFile = os.getcwd() + "/contest-work-sample-small"
        #self.logAdd("Current file: " + workFile)
        workFile = self.fillElementByName("attachment", workFile)
        self.clickElementById("send-contest-submit")
        self.assertBodyTextPresent(u"Ошибка отправки решения")
        self.assertPhpErrors()
        os.remove(workFile)
        
        #send large file
        """
        TODO: bug #911
        with open('contest-work-sample-large', 'w') as f:
            f.write('Q' * 40000000) 
        
        
        workFile = os.getcwd() + "/contest-work-sample-large"
        workFile = self.fillElementByName("attachment", workFile)
        self.clickElementById("send-contest-submit")
        #self.assertBodyTextPresent(u"...")
        self.assertPhpErrors()
        os.remove(workFile)
        """
        
        #Finally send normal file
        with open('contest-work-sample-normal', 'w') as f:
            f.write('Q' * 2*1000*1000) 
        
        
        workFile = os.getcwd() + "/contest-work-sample-normal"
        workFile = self.fillElementByName("attachment", workFile)
        self.clickElementById("send-contest-submit")
        self.assertBodyTextPresent(u"Спасибо, Ваше решение принято!")
        self.assertPhpErrors()
        os.remove(workFile)
        
        #Send a link
        self.gotoUrlByLinkText(u"Отправить решение")
        inpLink = u"Бла-бла-бла" + random_crap.randomText(6)
        inpLink = self.fillElementByName("fileexchange", inpLink)
        self.clickElementById("send-contest-submit")


        self.assertBodyTextPresent(u"Спасибо, Ваше решение принято!")
        self.assertPhpErrors()
        
 