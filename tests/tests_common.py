#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback, time

import selenium_test

def performLogin(test, login, password):
	"""
	returns True if login was successful
	"""
	if test is None:
		raise RuntimeError("Wrong webdriver parameter passed to performLogin. ")
	
	test.gotoRoot()
	
	print "login..."
	# assert we have no shit cookies here
	test.assertUrlNotPresent(u"Админка")
	
	authUrl = test.getUrlByLinkText(u"Авторизация")
	
	test.gotoSite(authUrl)
	
	test.assertSourceTextPresent(u"Логин")
	test.assertSourceTextPresent(u"Пароль")
	test.assertSourceTextPresent(u"Требуется аутентификация")
	
	#<input type="text" name="auth-login" />
	#ele = test.drv().find_element_by_name("auth-login")
	test.fillElementById("auth-login", login)
	test.fillElementById("auth-password", password)
	
	test.clickElementById("auth-submit")
	
	wrongAuth = test.checkSourceTextPresent(u"Пароль всё ещё неверный")
	return not wrongAuth
	
	#test.getUrlByLinkText(u"Админка")
	    
def performLogout(test):
	print "logout..."
	test.gotoPage("/?&mode=logout&ref=ladmin")
	
def performLoginAsAdmin(test, login, password):
	print "performLoginAsAdmin() called"
	performLogin(test, login, password)
	print "checking admin panel link"
	
	#check that we have entered the CP.
	# just chech that link exists.
	cpUrl = test.getUrlByLinkText(u"Админка")
	#test.gotoSite(cpUrl)
			