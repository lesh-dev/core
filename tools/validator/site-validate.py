#!/usr/bin/python

import httplib, urllib, re, os, sys

verboseMode = False
quietMode = False

def ReadPage(conn, url):
	request={
		"uri": 		url,
		"charset": 	"(detect automatically)",
		"doctype": 	"Inline",
		"group": 	"0"
	}

	params = urllib.urlencode(request)
	#print params

	conn.request("GET", "/check?" + params)

	# http://validator.w3.org/check?uri=http%3A%2F%2Ffizlesh.ru%2Fproduction-test&charset=%28detect+automatically%29&doctype=Inline&group=0
	r = conn.getresponse()
	#print r.status, r.reason
	if r.status != 200:
		raise RuntimeError("Cannot read page " + request["uri"])

	return r.read()
	#print data

def GetOutput(valid, errors, warns):
	text = str(len(errors)) + " error(s), " + str(len(warns)) + " warning(s)"
	if valid is None:
		text = "[ERROR] " + text
	elif valid and len(warns) == 0:
		text = "[OK] " + text
	elif valid and len(warns) > 0:
		text = "[WARN] " + text
	else:
		text = "[FAIL] " + text
	return text

def CheckPage(conn, page):	
	result = ReadPage(conn, page)
	valid, errors, warns = Validate(result)
	if not quietMode:
		print page + " " + GetOutput(valid, errors, warns)
	if verboseMode:
#		print "debug err = ",  errors
	
		for err in errors:
			print "Position: ", err["pos"]
			print "Error: ", err["msg"]

#		print "debug war = ", warns

		for warn in warns:
			print "Position: ", warn["pos"]
			print "Warning: ", warn["msg"]

	return valid, errors, warns

def CleanImage(text):
	return re.sub('<span class="err_type">(.+?)</span>', '', text)

def LineSpecBreak(text):
	m = re.search('<em>(.+?)</em>:.*?<span class="msg">(.*?)</span>(.*)',  text)
	if not m:
		raise RuntimeError("Not valid validator output. Please fix parser. Text: " + text)
	position = m.group(1).replace("  ", " ")
	errMsg = m.group(2).replace("&quot;", '"')
	crap = m.group(3)
	return {"pos": position, "msg": errMsg, "misc": crap}

def ParseErrors(result):
	errors = re.findall('<li class="msg_err">(.+?)</li>', result)
	errors = [CleanImage(x) for x in errors]
	errors = [LineSpecBreak(x) for x in errors]
	return errors

def ParseWarnings(result):
	warns = re.findall('<li class="msg_warn">(.+?)</li>', result)
	warns = [CleanImage(x) for x in warns]
	warns = [LineSpecBreak(x) for x in warns]
	return warns

def Validate(result):
	result = result.replace("\n","")
#	print "DEBUG: Page head: ", result[:500]
	m = re.search("<title>(.+?)</title>", result)
	if not m:
		return None, [{"pos": None, "msg": "Validation failed - no title tag in result. "}], []
	title = m.group(1).strip()
	if not "[Valid]" in title and not "[Invalid]" in title:
		return None, [{"pos": None, "msg": "Validation failed, probably page not found. "}], []
#	print "Page title: ", title
	errorList = ParseErrors(result)
	warnList = ParseWarnings(result)
	return "[Invalid]" not in title, errorList, warnList

args = sys.argv[:]

if "-v" in args or "--verbose" in args:
	verboseMode = True
	args = filter(lambda x: x != "-v" and x != "--verbose", args)

# quiet overrides verbosity.

if "-q" in args or "--quiet" in args:
	args = filter(lambda x: x != "-q" and x != "--quiet", args)
	quietMode = True
	verboseMode = False

if len(args) < 2:
	print "Syntax: " + args[0] + "[-v|--verbose] [-q|--quiet] <url>";
	sys.exit(1)

conn = httplib.HTTPConnection("validator.w3.org")
r = CheckPage(conn, args[1])
if not r[0]:
	sys.exit(2)
