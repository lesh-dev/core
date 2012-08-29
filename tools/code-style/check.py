#!/usr/bin/python

import os
import sys
import re

def print_bad_context(lines, index, message):
    line_count = len(lines)
    print "* * *", message
    for i in range(index - 3, index + 3):
        if i < 0 or i >= line_count:
            continue
        if i != index:
            print ' ', lines[i].rstrip()
        else:
            print '>', lines[i].rstrip()

def check_tab_style(lines):
    line_count = len(lines)
    for i in range(line_count):
        line = lines[i]
        sm = re.search('^[ ]+', line)
        if sm:
            spaces = sm.group()
            if len(spaces) % 4 != 0:
                print_bad_context(lines, i, "Invalid spaces count: %d" % len(spaces))
        tm = re.search('\t', line)
        if tm:
            print_bad_context(lines, i, "Tab detected")


def check_file(name):
    lines = []
    with open(name) as f:
        for line in f:
            lines.append(line)

    check_tab_style(lines)

def print_usage():
    print "Syntax: " + sys.argv[0] + " <file-name-to-check>"
    sys.exit(1)


if len(sys.argv) < 2:
    print_usage()

check_file(sys.argv[1])
