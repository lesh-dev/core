#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback

import selenium_test

def performLogin(test, login, password):
	if test is None:
		raise RuntimeError("Wrong webdriver parameter passed to performLogin. ")
	
	test.gotoPage("/")
	
	authUrl = test.getUrlByLinkText(u"Авторизация")
	
	test.gotoSite(authUrl)
	
	test.assertSourceTextPresent(u"Логин")
	test.assertSourceTextPresent(u"Пароль")
	test.assertSourceTextPresent(u"Требуется аутентификация")
	
	#<input type="text" name="auth-login" />
	#ele = test.drv().find_element_by_name("auth-login")
	test.fillElementByName("auth-login", login)
	test.fillElementByName("auth-password", password)
	
	test.clickElementByName("auth-form")
	
	#check that we have entered the CP.
	# just chech that link exists.
	test.getUrlByLinkText(u"Админка")
	
	#test.gotoSite(cpUrl)
	#test.assertBodyTextPresent(u"Пользователи")
    
def performLoginAsAdmin(test, login, password):
	performLogin(test, login, password)
	
	cpUrl = test.getUrlByLinkText(u"Админка")
	test.gotoSite(cpUrl)
	
	test.assertBodyTextPresent(u"Пользователи")
		