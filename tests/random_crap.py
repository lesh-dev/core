#!/usr/bin/python
# -*- coding: utf8 -*-

import random

# helper functions for random crap generation
# all module is API.

rusAlphaSmall = u"абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
rusAlphaCap = u"АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
engAlphaSmall = "abcdefgiklmnopqrstuvwxyz"
engAlphaCap = "ABCDEFGHIKLMNOPQRSTUVWZYZ"

specialCharsDefault = '.,!?;:"<>-=@%$^&*()\''
specialCharsWoAngle = '.,!?;:"-=@%$^&*()\''


def random_text(length):
    rs = ""
    for i in range(0, length):
        rs = rs + random.choice('abcdef0123456789')
    return rs


def phone():
    return "+7" + randomDigits(9)


def email():
    return random_text(7) + "@" + random_text(5) + ".ru",


def randomEmail():
    # FIXME: DEPRECATED, use email()
    return "mail_test_" + random_text(8) + "@example.com"


def date():
    return randomDigits(2) + "." + randomDigits(2) + "." + randomDigits(4)


def randomVkontakte():
    return "http://vk.com/id" + randomDigits(10)


def randomWord(length, wordOptions=None, specialChars=specialCharsDefault):

    if not wordOptions:
        wordOptions = []

    if "english" in wordOptions:
        enLang = True
    else:
        enLang = (random.randint(0, 10) < 7)

    if random.randint(0, 10) < 3:
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
            rs += random.choice(engAlphaSmall)
        else:
            rs += random.choice(rusAlphaSmall)

    if random.choice(range(0, 20)) < 3:
        rs += random.choice(specialChars)

    return rs


def randomDigits(length):
    rs = ""
    for i in range(0, length):
        rs += str(random.choice('0123456789'))
    return rs


def randomCrap(wordNumber, crapOptions=None, specialChars=specialCharsDefault):
    rs = ""
    for i in range(0, wordNumber):
        separator = " "
        if not crapOptions:
            crapOptions = []
        if "multiline" in crapOptions:
            if random.random() < 0.2:
                separator = "\n"
        if rs != "":
            rs += separator
        wordLen = random.randint(3, 10)
        rs += randomWord(wordLen, crapOptions, specialChars)
    return rs
