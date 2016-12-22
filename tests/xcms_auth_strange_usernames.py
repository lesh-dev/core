#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import xtest_common
import random_crap


class XcmsAuthStrangeUsernames(xtest_common.XcmsTest):
    """
    #905

    *positive cases
    <whatever>.user.<whatever>
    <whatever>.user
    user.<whatever>

    *negative cases
    .<whatever>
    @<whatever>
    ../usr/login

    """

    def run(self):
        
        self.ensure_logged_off()
        
        #positive cases

        inpLogin = "an_test_user_" + ".user." + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpPass = random_crap.random_text(10)
        inpName = u"Вася Пупкин" + random_crap.random_text(6)
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)
        logging.info("Created a new user: "+ inpLogin)
              
               
        inpLogin = "a" + random_crap.random_text(8) + ".user" 
        inpEMail = random_crap.randomEmail()
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)
        logging.info("Created a new user: "+ inpLogin)

         
        inpLogin = "user." + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName)
        logging.info("Created a new user: "+ inpLogin)

        #negative cases

        logging.info("Reached negative cases")
        
        inpLogin = ".user." + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName, "do_not_validate")
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: "+ inpLogin)
        self.performLogout() 
        
        inpLogin = "@user." + random_crap.random_text(8)
        inpEMail = random_crap.randomEmail()
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName, "do_not_validate")
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: "+ inpLogin)
        self.performLogout() 
        
        inpLogin = "../usr/login" 
        inpEMail = random_crap.randomEmail()
        inpLogin, inpEMail, inpPass, inpName = self.createNewUser(inpLogin, inpEMail, inpPass, inpName, "do_not_validate")
        self.assertBodyTextPresent(u"Имя пользователя должно начинаться с буквы или цифры")
        logging.info("Failed to create a new user: "+ inpLogin)
        self.performLogout() 
