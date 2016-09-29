#!/usr/bin/python

"""
Stupid code style checker.
Author: Mikhail Veltishchev <dichlofos-mv@yandex.ru>

Please do not forget to sync changes in `lesh` and `dmvn` style checkers:
* https://github.com/lesh-dev/core/tools/code-style
* https://bitbucket.org/dmvn-corp/dmvn.mexmat.net/tools/code_style
"""

import sys
import re

PHP_FILES = [
    'php',
    'code',
    'xcms',
]


def print_bad_context(lines, bad_lines):
    line_count = len(lines)
    skip = True
    for i in range(line_count):
        l = lines[i].rstrip()
        ln = i + 1
        if i in bad_lines:
            print '      ', bad_lines[i]
            print '%3d > %s' % (ln, l)
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


# removes quoted strings from code
def remove_strings(line):
    # remove double quotes
    line = re.sub(r'".*?"', '', line)
    # remove single quotes
    line = re.sub(r"'.*?'", '', line)
    return line


# removes JS-style regexps from code
def remove_js_regexps(line):
    # remove double quotes
    line = re.sub(r'/[^/]+/\.test\(', '', line)
    return line


# removes commas with HTML tags after them
def remove_commas_in_html(line):
    # remove cases like 'some words,<br/>'
    line = re.sub(r',<', '', line)
    return line


def remove_html_attributes(line):
    line = re.sub(
        r' (class|href|width|rows|cols|style|id|name|placeholder|'
        r'value|action|method|enctype|alt|src|type|title)="',
        ' \\1"',
        line
    )
    return line


# convert all possible operators to one form
def convert_operators(line):
    line = line.replace('===', '=')
    line = line.replace('==', '=')
    return line


# removes bash arrays file{a,bc}
def remove_file_expansions(line):
    line = re.sub(r'\{[$a-zA-Z0-9._,-]*?\}', '', line)
    return line


class BadLines(object):
    def __init__(self):
        self.bad_lines = dict()

    def add(self, message, index):
        if index not in self.bad_lines:
            self.bad_lines[index] = []
        self.bad_lines[index].append(message)

    def lines(self):
        return self.bad_lines


def check_code_style(lines, file_type):
    line_count = len(lines)
    bad_lines = BadLines()

    for index in range(line_count):
        line = lines[index]

        if not len(line) or line == "\n":
            continue

        # line endings check
        lem = re.match('^[^\x0A\x0D]+[\n]$', line)
        if not lem:
            lem = re.match('^[^\x0A\x0D]+$', line)
            # okay, last line may contain no CR-LF chars
            if not lem:
                bad_lines.add("UNIX-style line endings only allowed", index)

        # spaces count check
        sm = re.search('^[ ]+', line)
        if sm:
            spaces = sm.group()
            if len(spaces) % 4 != 0:
                ls = line.lstrip()
                if ls[0:2] == '* ' or ls == '*\n' or ls[0:3] == '/**' or ls[0:3] == '**/':
                    # okay, it seems like a Doxygen comment (TODO: add entrance/leave) check)
                    pass
                else:
                    bad_lines.add("Invalid spaces count: {}".format(len(spaces)), index)

        # tab check
        tm = re.search('\t', line)
        if tm:
            bad_lines.add("No tabs allowed", index)

        # shorttag check
        stm = re.search('<[?][^px]', line)
        if not stm:
            stm = re.search('<[?]$', line)
        if stm:
            bad_lines.add("No PHP shorttags allowed", index)

        # if+( ugly style check
        itm = re.search(' ?if\(', line)
        if not itm:
            itm = re.search(' ?elseif\(', line)
        if not itm:
            itm = re.search(' ?foreach\(', line)
        if not itm:
            itm = re.search(' ?for\(', line)
        if not itm:
            itm = re.search(' ?while\(', line)
        if itm:
            bad_lines.add("if/elseif/for/foreach/while clause should be separated from condition braces", index)

        line_cleanup = line
        line_cleanup = remove_html_attributes(line_cleanup)
        line_cleanup = remove_strings(line_cleanup)
        line_cleanup = remove_js_regexps(line_cleanup)
        line_cleanup = remove_file_expansions(line_cleanup)
        line_cleanup = remove_commas_in_html(line_cleanup)
        line_cleanup = convert_operators(line_cleanup)
        line_cleanup = re.sub(r',$', '', line_cleanup)

        # missing spaces after commas
        sac = re.search(r',[^ ]', line_cleanup)
        if sac:
            bad_lines.add("Commas should contain spaces after them", index)

        # trailing spaces check
        ts = re.search('[^ ]+[ ]+$', line)
        if ts:
            bad_lines.add("No trailing spaces allowed", index)

        # forbidden PHP operators
        if file_type in PHP_FILES:
            empty_op = re.search('[^a-zA-Z_]empty\(', line)
            if empty_op:
                bad_lines.add("Operator 'empty' is forbidden for " + str(PHP_FILES) + " files", index)

            nsbe = re.search(r'([^|+<>!. ]=|=[^ >\n]|=>[^ ])', line_cleanup)
            if nsbe:
                bad_lines.add("Assignment/comparison/key-value (=>) operators should be surrounded with spaces", index)

    print_bad_context(lines, bad_lines.lines())
    # return 1 if there some errors
    if len(bad_lines.lines()):
        return 1
    return 0


def check_file(name):
    lines = []
    ft_match = re.search('\.([a-z]+)$', name)
    file_type = 'unknown'
    if ft_match:
        file_type = ft_match.group(1)
    with open(name) as f:
        for line in f:
            lines.append(line)

    return check_code_style(lines, file_type)


def print_usage():
    print "Syntax: " + sys.argv[0] + " <file-name-to-check>"
    sys.exit(1)


if len(sys.argv) < 2:
    print_usage()

result = check_file(sys.argv[1])
sys.exit(result)
