#!/usr/bin/python
# -*- coding: utf8 -*-

import logging
import os


# Bells-And-Whistles (tm) Python 2.x library
# Contains non-categorized common crap code used in selenium tests.


def configure_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # remove all default handlers
    root_logger.handlers = []

    # and clear output
    all_tests_log_path = "logs/all_tests.log"
    try:
        os.makedirs(os.path.dirname(all_tests_log_path))
        os.unlink(all_tests_log_path)
    except Exception:
        pass

    formatter = logging.Formatter("%(asctime)s|%(levelname)-8s %(message)s")

    file_handler = logging.FileHandler(all_tests_log_path)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def set_logger_file_output(file_name):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.acquire()
            handler.stream.close()
            handler.stream = open(file_name, handler.mode)
            handler.release()


class BawError(RuntimeError):
    pass


def read_file(file_name):
    contents = ""
    with open(file_name) as f:
        contents = f.read()
    return contents


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
