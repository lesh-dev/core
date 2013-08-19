#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, re, commands, string

QuotaThresholdPercent = 95

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
    return "{0}%".format(round(perc, 1))
    
def bQuotaExceededForLine(line):
    m = re.search("(\S+)\s+(\d+)\s*(\w)", line)
    if not m:
        return False
    
    path = m.group(1).strip()
    sizeLog = int(m.group(2))
    scaleLog = m.group(3).upper().strip()
    scales = {
        "": 1,
        "K": 1024,
        "M": 1024*1024,
        "G": 1024*1024*1024,
        "T": 1024*1024*1024*1024,
        "P": 1024*1024*1024*1024*1024
        }
    if scaleLog not in scales:
        raise RuntimeError("Incorrect size format for line '" + line + "'. ")
    maxSize = sizeLog * scales[scaleLog];
    
    realSize = int(commands.getoutput("du -sb " + path).strip().split()[0])
    #print "max size for ", line, ": ", maxSize, " real size: ", realSize
    if bQuotaExceeded(realSize, maxSize):
        print "Quota exceeded for path " + path + " by " + getExceedPercent(realSize, maxSize)
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