#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, re, commands

QuotaThresholdPercent = 95

def isList(x):
    return type(x) == type(list())

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
    perc = (realSize * 100 / maxSize) - 100.0
    return "{0}%".format(decimal(perc))

def decimal(n):
    return round(n, 1)

def getHumanValue(number):
    k = 1024
    if number < k**1: return str(number)
    if number < k**2: return str(decimal(number/k**1)) + "K"
    if number < k**3: return str(decimal(number/k**2)) + "M"
    if number < k**4: return str(decimal(number/k**3)) + "G"
    if number < k**5: return str(decimal(number/k**4)) + "T"
    return str(decimal(number/k**5)) + "P"

def bQuotaExceededForLine(line):
    m = re.search("(\S+)\s+(\d+)\s*(\w)", line)
    if not m:
        return False

    path = m.group(1).strip()
    sizeLog = int(m.group(2))
    scaleLog = m.group(3).upper().strip()
    k = 1024
    scales = {
        "" : k**0,
        "K": k**1,
        "M": k**2,
        "G": k**3,
        "T": k**4,
        "P": k**5
        }
    if scaleLog not in scales:
        raise RuntimeError("Incorrect size format for line '" + line + "'. ")
    maxSize = sizeLog * scales[scaleLog];

    res, output = getCommandOutput(["du", "-sb", path]);
    if res != 0:
        raise RuntimeError("Error occured on getting disk usage for line '" + line + "'. ")

    realSize = int(output.strip().split()[0])
    #print "max size for ", line, ": ", maxSize, " real size: ", realSize
    if bQuotaExceeded(realSize, maxSize):
        print "Quota " + getHumanValue(maxSize) + " exceeded for path " + path + " by " + getExceedPercent(realSize, maxSize)
        return True
    return False

def monitor(fileList):
    quotaExceeded = False
    for line in open(fileList):
        try:
            if bQuotaExceededForLine(line.strip()):
                quotaExceeded = True
        except ValueError:
            print "Something is wrong on line " + line
            return 2
        except RuntimeError as e:
            print e
            return 2

    if quotaExceeded:
        return 1
    return 0;

if len(sys.argv) < 2:
    print "Parameters not set. Syntax: quota-monitor.py <directory-list>"
    sys.exit(2)

fileList = sys.argv[1]

try:
    sys.exit(monitor(fileList))
except IOError as e:
    print "Exception occured in monitor: ", e
    sys.exit(2)
