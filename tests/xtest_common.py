#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium import webdriver
import os, sys, traceback, time

import selenium_test, random_crap

def isInstallerPage(test):
	return test.curUrl().endswith("install.php")

def assertNoInstallerPage(test):
	test.gotoRoot()
	if isInstallerPage(test):
		raise selenium_test.TestFatal("Installer page detected, while we did not expected it. You should run this test on installed XCMS. ")


def gotoAuthLink(test):
	test.logAdd("xtest_common.gotoAuthLink: going to authenticate. ")
	test.gotoUrlByLinkText(u"Авторизация")

def gotoAdminPanel(test):
	test.logAdd("xtest_common.gotoAdminPanel: going to admin control panel. ")
	test.gotoUrlByLinkText(u"Админка")

def gotoCabinet(test):
	test.logAdd("xtest_common.gotoCabinet: going to user control panel (cabinet). ")
	test.gotoUrlByLinkText(u"Личный кабинет")

def getAuthLink(test):
	return test.getUrlByLinkText(u"Авторизация")

def gotoBackToAnketaView(test):
	test.gotoUrlByLinkText(u"Вернуться к просмотру участника")

def gotoBackAfterComment(test):
	#test.gotoUrlByLinkText(u"Вернуться к списку комментов") # older variant
	gotoBackToAnketaView(test)
	
def getAdminPanelLink(test):
	return test.getUrlByLinkText(u"Админка")

def performLogoutFromSite(test):
	test.gotoUrlByLinkText(u"Выход")

def performLogoutFromAdminPanel(test):
	test.gotoUrlByLinkText(u"Выйти")

def performLogin(test, login, password):
	"""
	returns True if login was successful
	"""
	if test is None:
		raise RuntimeError("Wrong webdriver parameter passed to performLogin. ")
	
	test.addAction("user-login", login + " / " + password)
#	test.logAdd("performLogin(" + login + ", " + password + ")")

	print "performLogin(): goto root"
	
	test.gotoRoot()
	
	# assert we have no shit cookies here
	test.assertUrlNotPresent(u"Админка", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")
	test.assertUrlNotPresent(u"Личный кабинет", "Here should be no auth cookies. But they are. Otherwise, your test is buggy and you forgot to logout previous user. ")
	
	gotoAuthLink(test)
	
	test.assertSourceTextPresent(u"Логин")
	test.assertSourceTextPresent(u"Пароль")
	test.assertSourceTextPresent(u"Требуется аутентификация")
	
	#<input type="text" name="auth-login" />
	#ele = test.drv().find_element_by_name("auth-login")
	test.fillElementById("auth-login", login)
	test.fillElementById("auth-password", password)
	
	test.clickElementById("auth-submit")
	
	wrongAuth = test.checkSourceTextPresent([u"Пароль всё ещё неверный", "Wrong password"])
	if wrongAuth:
		return False
	
	# now let's check that Cabinet link and Exit link are present. if not - it's a bug.

	test.assertUrlPresent(u"Выход", "Here should be logout link after successful authorization. ")
	test.assertUrlPresent(u"Личный кабинет", "Here should be Cabinet link after successful authorization. ")
	
	return True
		    
def performLogout(test):
	print "performLogout()"
	test.addAction("user-logout")
	test.gotoPage("/?&mode=logout&ref=ladmin")
	
def performLoginAsAdmin(test, login, password):
	print "performLoginAsAdmin(" + login + ", " + password + ")"
	if not performLogin(test, login, password):
		print "Admin authorization failed"
		raise selenium_test.TestError("Cannot perform Admin authorization as " + login + "/" + password)
		
	print "performLoginAsAdmin(): checking admin panel link"
	
	#check that we have entered the CP.
	# just chech that link exists.
	cpUrl = getAdminPanelLink(test)
	#test.gotoSite(cpUrl)
	
	
def createNewUser(test, conf, login, email, password, name, auxParams = []):
	print "createNewUser(" + login + ", " + email + ", " + password + ", " + name + ")"
	
	performLoginAsAdmin(test, conf.getAdminLogin(), conf.getAdminPass())
	
	print "go to user creation panel"
	
	#	test.gotoRoot()
	gotoAdminPanel(test)
	
	gotoUserList(test)
	
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
	
	profileLink = inpLogin
	# TODO, SITE BUG: make two separate links
	test.gotoUrlByPartialLinkText(profileLink)

	test.assertBodyTextPresent(u"Учётные данные")
	test.assertBodyTextPresent(u"Привилегии")

	# temporary check method
	# test user login
	test.assertTextPresent("//div[@class='user-ops']", inpLogin)
	# test user creator (root)
	test.assertTextPresent("//div[@class='user-ops']", conf.getAdminLogin())
	test.assertElementValueById("name-input", inpName)
	test.assertElementValueById("email-input", inpEMail)
	
	#logoff root
	performLogout(test)
	
	return inpLogin, inpEMail, inpPass, inpName
	

def addCommentToPerson(test):
	test.gotoUrlByLinkText(u"Добавить комментарий")
	commentText = random_crap.randomText(40) + "\n" + random_crap.randomText(50) + "\n" + random_crap.randomText(30)
	
	commentText = test.fillElementByName("comment_text", commentText)

	test.clickElementByName("update-person_comment")
	test.assertBodyTextPresent(u"Комментарий успешно сохранён")
	gotoBackToAnketaView(test)
	return commentText
	
def editCommentToPerson(test, commentLinkId):
	test.gotoUrlByLinkId("comment-edit-1")
	oldCommentText = test.getElementValueByName("comment_text")
	newCommentText =  random_crap.randomText(10) + "\n" + oldCommentText + "\n" + random_crap.randomText(6)
	newCommentText = test.fillElementByName("comment_text", newCommentText)
	test.clickElementByName("update-person_comment")
	test.assertBodyTextPresent(u"Комментарий успешно сохранён")
	gotoBackToAnketaView(test)
	return newCommentText

def setTestNotifications(test, emailString, adminLogin, adminPass):
	performLoginAsAdmin(test, adminLogin, adminPass)
	gotoAdminPanel(test)
	test.gotoUrlByLinkText(u"Уведомления")

	test.fillElementById("edtg_user-change", emailString);
	test.fillElementById("edtg_content-change", emailString);

	test.fillElementById("edtg_reg", emailString);

	test.fillElementById("edtg_reg-test", emailString);
	test.fillElementById("edtg_reg-managers", emailString);
	test.fillElementById("edtg_reg-managers-test", emailString);
	
	test.clickElementById("editTag")
	performLogout(test)


def gotoUserList(test):
	test.logAdd("Navigating to user list from admin CP. ")
	test.gotoUrlByLinkText(u"Пользователи")
	test.assertBodyTextPresent(u"Администрирование пользователей")

	
	


	


