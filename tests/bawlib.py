#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import os


def configure_logger():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# Bells-And-Whistles (tm) Python 2.x library
# Contains non-categorized common crap code used in selenium tests.


class BawError(RuntimeError):
    pass


class CliParamError(BawError):
    pass


def fileBaseName(fileName):
    return os.path.basename(fileName)


def wrapIfLong(text):
    # maxLen in userSerialize + epsilon
    if len(text) > 80:
        return "\n" + text
    return text


def cut_http(link):
    return link.replace('http://', '').replace('https://', '')


def userSerialize(text, options=None):
    if not options:
        options = []
    if is_list(text):
        return "|".join([userSerialize(x) for x in text])
    if isString(text):
        if "cut_strings" in options or "cut_string" in options:
            maxLen = 75
            if len(text) > maxLen:
                return "'" + text[:maxLen] + "...'"
            else:
                return "'" + text + "'"
        return "'" + text + "'"
    if isBool(text):
        if text:
            return "TRUE"
        else:
            return "FALSE"
    return str(text)


def is_list(x):
    return isinstance(x, list)


def isString(x):
    return isinstance(x, str) or isinstance(x, unicode)


def isBool(x):
    return isinstance(x, bool)


def isNumber(x):
    return isinstance(x, int) or isinstance(x, long)


def isEqual(x, y):
    if isString(x) and isString(y):
        return (x.strip() == y.strip())
    else:
        raise RuntimeError(
            "Cannot compare anything except strings, sorry. Type of X is " + str(type(x)) +
            ", and type of Y is " + str(type(y)) + "."
        )


def isVoid(x):
    if is_list(x):
        return (not x)
    else:
        return x is None or x.strip() == ""
