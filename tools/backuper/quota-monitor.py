#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import re
import commands

QuotaThresholdPercent = 95


def isList(x):
    return (type(x) == type(list()))


def isVoid(x):
    return (x.strip() == "")


# python 2.7+
#def getCommandOutput(command):
    #if not isList(command):
        #command = command.split()
    #try:
        #output = subprocess.check_call(command)
        #return 0, output
    #except subprocess.CalledProcessError as e:
        #return e.returncode, e.output


# we have python 2.6 only.
def getCommandOutput(command):
    if isList(command):
        command = " ".join(command)
    return commands.getstatusoutput(command)


def bQuotaExceeded(realSize, maxSize):
    if maxSize == 0:
        return False
    perc = (realSize * 100 / maxSize)
    if perc > QuotaThresholdPercent:
        return True
    return False


def getExceedPercent(realSize, maxSize):
    if maxSize == 0:
        return 0
    return (realSize * 100 / maxSize) - 100.0


def formatExceedPercent(perc):
    return "{0}%".format(decimal(perc))


def decimal(n):
    return round(n, 1)


def getHumanValue(number):
    k = 1024
    if number < k**1:
        return str(number)
    if number < k**2:
        return str(decimal(number/k**1)) + "K"
    if number < k**3:
        return str(decimal(number/k**2)) + "M"
    if number < k**4:
        return str(decimal(number/k**3)) + "G"
    if number < k**5:
        return str(decimal(number/k**4)) + "T"
    return str(decimal(number/k**5)) + "P"


def bQuotaExceededForLine(line):
    line = line.strip()
    # skip commented lines
    if line[0:1] == "#":
        return False

    m = re.search("(\S+)\s+(\d+)\s*(\w+)", line)
    if not m:
        if not isVoid(line):
            print "Line " + line + " has incorrect format. "
        return False

    path = m.group(1).strip()
    try:
        sizeLog = int(m.group(2).strip())
    except ValueError as e:
        print "Something is wrong on line '" + line + "': "
        print e
        raise

    scaleLog = m.group(3).upper().strip()
    k = 1024
    scales = {
        "":  k**0,
        "B":  k**0,

        "K":  k**1,
        "KB": k**1,

        "M":  k**2,
        "MB":  k**2,

        "G":  k**3,
        "GB":  k**3,

        "T":  k**4,
        "TB":  k**4,

        "P":  k**5,
        "PB":  k**5
        }
    if scaleLog not in scales:
        raise RuntimeError("Incorrect size format for line '" + line + "'. ")
    maxSize = sizeLog * scales[scaleLog]

    res, output = getCommandOutput(["du", "-sb", path])
    if res != 0:
        raise RuntimeError("Error occured on getting disk usage for line '" + line + "':\n" + output)

    outList = output.strip().split()
    if outList:
        try:
            realSize = int(outList[0])
        except ValueError as e:
            print "du returned crap as datasize: '" + outList[0] + " for line '" + line + "'."
            print "Exception:\n", e
            print "Full 'du -sb' output:\n" + output
            raise
    else:
        raise RuntimeError("DiskUsage returned success code, but empty output for line '" + line + "'. ")

    #print "max size for ", line, ": ", maxSize, " real size: ", realSize
    if bQuotaExceeded(realSize, maxSize):
        perc = getExceedPercent(realSize, maxSize)
        if perc < 0.0:
            print "Quota " + getHumanValue(maxSize) + " is about to be exceeded for path " + path
            print "Remaining quota: " + formatExceedPercent(-perc)
        else:
            print "Quota {quota} exceeded for path {path} by {value}".format(
                quota=getHumanValue(maxSize),
                path=path,
                value=formatExceedPercent(perc)
                )
        return True
    return False


def monitor(fileList):
    quotaExceeded = False
    for line in open(fileList):
        try:
            if bQuotaExceededForLine(line.strip()):
                quotaExceeded = True
        except ValueError as e:
            print "Checking aborted: shit happens on line " + line
            return 2
        except RuntimeError as e:
            print e
            return 2

    if quotaExceeded:
        return 1
    return 0


if len(sys.argv) < 2:
    print "Parameters not set. Syntax: quota-monitor.py <directory-list>"
    sys.exit(2)

fileList = sys.argv[1]

try:
    sys.exit(monitor(fileList))
except IOError as e:
    print "Exception occured in monitor: ", e
    sys.exit(2)
