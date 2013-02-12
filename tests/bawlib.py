#!/usr/bin/python
# -*- coding: utf8 -*-

import os

# Bells-And-Whistles (tm) Python 2.x library
# Contains non-categorized common crap code used in selenium tests.

class BawError(RuntimeError):
	pass

class CliParamError(BawError):
	pass

def fileBaseName(fileName):
	return os.path.basename(fileName)
	
def userSerialize(text):
	if isList(text):
		return "|".join(text)
	return str(text)

def isList(x):
	return type(x) == type(list())

def isString(x):
	return type(x) == type("string") or type(x) == type(u"string")

def isEqual(x, y):
	if isString(x) and isString(y):
		return (x.strip() == y.strip())
	else:
		raise RuntimeError("Cannot compare anything except strings, sorry. Type of X is " + str(type(x)) + ", and type of Y is " + str(type(y)) + ".")

def isVoid(x):
	return x is None or x.strip() == ""
	
	
# simple command line framework
def argMatchOption(value, optSpec):
	"""
		"value" == "optSpec" or value in [optSpec]
	"""
	if isString(optSpec):
		return value == optSpec
	elif isList(optSpec):
		return value in optSpec
	else:
		raise RuntimeError("argMatchOption got optSpec parameter, which is neither string list, nor single string. ")
	
def getOption(opt, inArgs):
	"""
		gets option list 'args' and option name 'opt' (or list of synonyms).
		returns: option value plus filtered arg list.
		sample: args = [-a, --name, qqq, -b], opt = --name
		returns 'qqq', [-a, -b]
	"""
	args = inArgs[:]
	for i in xrange(0, len(args)-1):
		if argMatchOption(args[i], opt):
			del args[i]
			value = args[i]
			del args[i]
			return value, args
	# check last argument match
	if argMatchOption(args[-1], opt):
		raise CliParamError("Option " + userSerialize(opt) + " specified without argument. ")
	return None, args

def getSingleOption(opt, inArgs):
	"""
		gets option name (or synonym list) and arg list.
		returns True if found (or False if not) and changed list.
	"""
	args = inArgs[:]
	for i in xrange(0, len(args)):
		if argMatchOption(args[i], opt):
			del args[i]
			return True, args
	return False, args
	