#!/usr/bin/env python
# -*- coding: utf8 -*-

# this tool searches backup folder and leaves only backups on 'exponential' time scale.

import sys
import os
import re
import datetime
import shutil

ExpPowerBase = 1.2


def isBackupDir(x):
    name = os.path.basename(x)
    m = re.match("\d\d\d\d-\d\d-\d\d", name)
    return True if m else False


def getBackupList(baseDir):
    dirList = filter(os.path.isdir, [os.path.join(baseDir, x) for x in os.listdir(baseDir)])
    backupList = sorted(filter(isBackupDir, dirList))
    backupList.reverse()
    return backupList


def parseDate(name):
    try:
        m = re.match("(\d+)-(\d+)-(\d+)", name)
        if not m:
            raise RuntimeError("Cannot parse date format for '" + name + "'. ")
        if m.groups < 3:
            raise RuntimeError("Cannot parse date format for '" + name + "' (matches count less than 3). ")

        (year, month, day) = (int(x) for x in m.group(1, 2, 3))
        return datetime.datetime(year, month, day)

    except (ValueError, RuntimeError):
        sys.stderr.write("Warning: cannot parse backup date '" + name + "'. Skipping this directory.\n")
        return None


def extractDate(x):
    return parseDate(os.path.basename(x))


def getRemoveList(backupList):
    if not backupList:
        return []

    # it is reverse-sorted, latest is first
    firstBackupDate = extractDate(backupList[0])
    if not firstBackupDate:
        raise RuntimeError("Latest backup directory has incorrect format. ")

    remainDates = set([firstBackupDate])

    # make exponential backup row - from latest
    days = 0
    power = 0
    while days < len(backupList):
        days = int(ExpPowerBase ** power)
        power += 1
        leaveDate = firstBackupDate - datetime.timedelta(days=days)
        remainDates.add(leaveDate)

    removeList = []
    for x in backupList:
        date = extractDate(x)
        if date and date not in remainDates:
            removeList.append(x)

    return removeList

# -------------------------------
cmdArgs = sys.argv[1:]

if not cmdArgs:
    print "Sorry, no parameters. Syntax: backup-filter.py [-l|--list-only] <directory-to-clean>"
    sys.exit(2)

doListOnly = False

if cmdArgs[0] == "-l" or cmdArgs[0] == "--list-only":
    doListOnly = True
    cmdArgs.pop(0)

if not cmdArgs:
    print "Sorry, 'directory-to-clean' not specified. Syntax: backup-filter.py [-l|--list-only] <directory-to-clean>"
    sys.exit(2)

baseDir = cmdArgs.pop(0)
if cmdArgs:
    print "Error: trailing command-line parameters detected. Switches should preceed <path-to-clean>."
    sys.exit(2)

#print "Removing backups in directory " + baseDir
backupList = getBackupList(baseDir)
toRemove = getRemoveList(backupList)
#    print len(backupList), len(toRemove)

if doListOnly:
    if toRemove:
        print "\n".join(toRemove)
else:
    for x in toRemove:
        shutil.rmtree(x)
