#!/usr/bin/python
# -*- coding: utf8 -*-

import random

# helper functions for random crap generation
# all module is API.

rusAlphaSmall = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
rusAlphaCap = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
engAlphaSmall = "abcdefgiklmnopqrstuvwxyz"
engAlphaCap = "ABCDEFGHIKLMNOPQRSTUVWZYZ"

def randomText(length):
	rs = ""
	for i in range(0, length):
		rs = rs + random.choice('abcdef0123456789')
	return rs	

def randomEmail():
	return "mail_test_" + randomText(8) + "@example.com"
		
def randomVkontakte():
	return "http://vk.com/id" + randomDigits(10)
	
def randomWord(length):
	rs = ""
	
	enLang = (random.randint(0,10) < 7)
	
	if random.randint(0,10) < 3:
		if enLang:
			rs = random.choice(engAlphaCap)
		else:
			rs = random.choice(rusAlphaCap)
	else:
		if enLang:
			rs = random.choice(engAlphaSmall)
		else:
			rs = random.choice(rusAlphaSmall)
	
	for i in range(0, length):
		if enLang:
			rs = rs + random.choice(engAlphaSmall)
		else:
			rs = rs + random.choice(rusAlphaSmall)
		
	if random.choice(range(0,20)) < 3:
		rs = rs + random.choice('.,!?;:"<>-==@%$^&*()')
			
	return rs	
		
def randomDigits(length):
	rs = ""
	for i in range(0, length):
		rs = rs + str(random.choice('0123456789'))
	return rs

def randomCrap(wordNumber, crapOptions = []):
	rs = ""
	for i in range(0, wordNumber):
		wordLen = random.randint(3,10)
		rs = rs + " " + randomWord(wordLen)
		if "multiLine" in crapOptions:
			if random.random() < 0.2:
				rs = rs + "\n"
	return rs
