#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback, time

import selenium_test

def performLogin(test, login, password):
	"""
	returns True if login was successful
	"""
	test.addAction("user-login", login + " / " + password)
#	test.logAdd("performLogin(" + login + ", " + password + ")")
	
	if test is None:
		raise RuntimeError("Wrong webdriver parameter passed to performLogin. ")
	
	test.gotoRoot()
	
	# assert we have no shit cookies here
	test.assertUrlNotPresent(u"Админка", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")
	
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
	
	wrongAuth = test.checkSourceTextPresent([u"Пароль всё ещё неверный", "Wrong password"])
	return not wrongAuth
	
	#test.getUrlByLinkText(u"Админка")
	    
def performLogout(test):
	print "logout..."
	test.addAction("user-logout")
	test.gotoPage("/?&mode=logout&ref=ladmin")
	
def performLoginAsAdmin(test, login, password):
	print "performLoginAsAdmin(" + login + ", " + password + ")"
	performLogin(test, login, password)
	print "checking admin panel link"
	
	#check that we have entered the CP.
	# just chech that link exists.
	cpUrl = test.getUrlByLinkText(u"Админка")
	#test.gotoSite(cpUrl)
	
	
def createNewUser(test, conf, login, email, password, name, auxParams = []):
	print "createNewUser(" + login + ", " + email + ", " + password + ", " + name + ")"
	
	performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
	
	print "go to user creation panel"
	
	#	test.gotoRoot()
	test.gotoUrlByLinkText(u"Админка")
	# navigate to users CP
	print "goto user list."
	test.gotoUrlByLinkText(u"Пользователи")
	test.assertBodyTextPresent(u"Администрирование пользователей")
	test.gotoUrlByLinkText(["Create user", u"Создать пользователя"])
	
	inpLogin = test.fillElementById("login", login)
	print "login = '" + inpLogin + "'"
	if inpLogin == "":
		raise RuntimeError("Filled login value is empty!")
	
	inpEMail = test.fillElementById("email", email)
	inpPass1 = test.fillElementById("password", password)
	print "original pass: '" + password + "'"
	inpPass2 = test.fillElementById("password_confirm", password)
	if inpPass1 != inpPass2:
		raise RuntimeError("Unpredicted input behavior on password entering")
	inpPass = inpPass1
	print "actual pass: '" + inpPass + "'"
	
	inpName = test.fillElementById("name", name)
	
	# set notify checkbox.
	test.clickElementByName("notify_user")
	# send form
	
	test.clickElementByName("create_user")
	
	
	if "do_not_validate" in auxParams:
		print "not validating created user, just click create button and shut up. "
		return inpLogin, inpEMail, inpPass, inpName

	print "user created, going to user list again to refresh. "
		
	test.assertBodyTextPresent(u"Пользователь успешно создан")
	# refresh user list
	test.gotoUrlByLinkText(u"Пользователи")
	
	# enter user profile
	print "entering user profile. "
	test.gotoUrlByLinkText(inpLogin)

	test.assertBodyTextPresent(u"Учётные данные")
	test.assertBodyTextPresent(u"Привилегии")

	# temporary check method
	# test user login
	test.assertTextPresent("//div[@class='user-ops']", inpLogin)
	# test user creator (root)
	test.assertTextPresent("//div[@class='user-ops']", conf.getAdminLogin())
	test.assertElementValueById("name", inpName)
	test.assertElementValueById("email", inpEMail)
	
	#logoff root
	performLogout(test)
	
	return inpLogin, inpEMail, inpPass, inpName

