#!/usr/bin/python

import os
import sys
import re

def print_bad_context(lines, bad_lines):
    line_count = len(lines)
    skip = True
    for i in range(line_count):
        l = lines[i].rstrip()
        ln = i + 1
        if i in bad_lines:
            print '      ', bad_lines[i]
            print '%3d > %s' % (ln, l) # , '#', bad_lines[i]
            skip = False
            continue
        if (i+2) in bad_lines or (i+1) in bad_lines:
            print '%3d   %s' % (ln, l)
            skip = False
            continue
        if (i-2) in bad_lines or (i-1) in bad_lines:
            print '%3d   %s' % (ln, l)
            skip = False
            continue
        if not skip:
            print '...'
            skip = True

def check_tab_style(lines):
    line_count = len(lines)
    bad_lines = dict()
    for i in range(line_count):
        line = lines[i]
        sm = re.search('^[ ]+', line)
        if sm:
            spaces = sm.group()
            if len(spaces) % 4 != 0:
                message = "Invalid spaces count: %d" % len(spaces)
                if i not in bad_lines:
                    bad_lines[i] = []
                bad_lines[i].append(message)
        tm = re.search('\t', line)
        if tm:
            message = "Tab detected"
            if i not in bad_lines:
                bad_lines[i] = []
            bad_lines[i].append(message)

        # shorttag check
        stm = re.search('<[?][^px]', line)
        if not stm:
            stm = re.search('<[?]$', line)
        if stm:
            message = "Shotrtag detected"
            if i not in bad_lines:
                bad_lines[i] = []
            bad_lines[i].append(message)


    print_bad_context(lines, bad_lines)
    # return 1 if there some errors
    if len(bad_lines) > 1:
        return 1
    return 0


def check_file(name):
    lines = []
    with open(name) as f:
        for line in f:
            lines.append(line)

    return check_tab_style(lines)

def print_usage():
    print "Syntax: " + sys.argv[0] + " <file-name-to-check>"
    sys.exit(1)


if len(sys.argv) < 2:
    print_usage()

result = check_file(sys.argv[1])
sys.exit(result)
