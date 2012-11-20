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

def check_code_style(lines):
    line_count = len(lines)
    bad_lines = dict()

    def add_bad_line(bad_lines, message, index):
        if index not in bad_lines:
            bad_lines[index] = []
        bad_lines[index].append(message)

    for i in range(line_count):
        line = lines[i]

        if not len(line) or line == "\n":
            continue

        # line endings check
        lem = re.match('^[^\x0A\x0D]+[\n]$', line)
        if not lem:
            lem = re.match('^[^\x0A\x0D]+$', line)
            # okay, last line may contain no CR-LF chars
            if not lem:
                add_bad_line(bad_lines, "UNIX-style line endings only allowed" , i)

        # spaces count check
        sm = re.search('^[ ]+', line)
        if sm:
            spaces = sm.group()
            if len(spaces) % 4 != 0:
                ls = line.lstrip()
                if ls[0:2] == '* ' or ls[0:3] == '/**' or ls [0:3] == '**/':
                    # okay, it seems like a Doxygen comment (TODO: add entrance/leave) check)
                    pass
                else:
                    add_bad_line(bad_lines, "Invalid spaces count: %d" % len(spaces), i)

        # tab check
        tm = re.search('\t', line)
        if tm:
            add_bad_line(bad_lines, "No tabs allowed", i)

        # shorttag check
        stm = re.search('<[?][^px]', line)
        if not stm:
            stm = re.search('<[?]$', line)
        if stm:
            add_bad_line(bad_lines, "No PHP shorttags allowed", i)

        # trailing spaces check
        ts = re.search('[^ ]+[ ]+$', line)
        if ts:
            add_bad_line(bad_lines, "No trailing spaces allowed", i)

    print_bad_context(lines, bad_lines)
    # return 1 if there some errors
    if len(bad_lines):
        return 1
    return 0


def check_file(name):
    lines = []
    with open(name) as f:
        for line in f:
            lines.append(line)

    return check_code_style(lines)

def print_usage():
    print "Syntax: " + sys.argv[0] + " <file-name-to-check>"
    sys.exit(1)


if len(sys.argv) < 2:
    print_usage()

result = check_file(sys.argv[1])
sys.exit(result)
