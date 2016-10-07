#!/usr/bin/python

"""
Stupid code style checker.
Author: Mikhail Veltishchev <dichlofos-mv@yandex.ru>

Please do not forget to sync changes in `lesh` and `dmvn` style checkers:
* https://github.com/lesh-dev/core/tools/code-style
* https://bitbucket.org/dmvn-corp/dmvn.mexmat.net/tools/code_style
"""

import re
import sys
import profile
import textwrap

import common

_DOUBLE_QUOTES = re.compile(r'".*?[^\\]"')
_SINGLE_QUOTES = re.compile(r"'.*?'")
_RE_HTML_ATTRIBUTES = re.compile(
    r' (class|href|width|height|rows|cols|colspan|style|id|name|placeholder|'
    r'value|action|method|enctype|accept|alt|src|target|type|language|title|'
    r'http-equiv|content|size|disabled|content|enum-type|row-id|color|'
    r'field-name)="'
)
_FILE_EXPANSIONS = re.compile(r'\{[$a-zA-Z0-9._,-]*?\}')
_JS_REGEXPS = re.compile(r'/[^/]+/\.test\(')

_LINE_ENDINGS = re.compile(r'^[^\x0A\x0D]+[\n]$')
_LINE_ENDINGS_LAST = re.compile(r'^[^\x0A\x0D]+$')

_SHORTTAG = re.compile(r'<[?][^px]')
_SHORTTAG_SHORT = re.compile(r'<[?]$')

_SPACES = re.compile(r'^[ ]+')
_SPACES_COMMAS = re.compile(r',[^ ]')
_TRAILING_SPACES = re.compile(r'[^ ]+[ ]+$')

_HTML_COMMAS = re.compile(r',<')
_COMMA_END = re.compile(r',$')

_UGLY_CONTROL = re.compile(r' ?(if|elseif|foreach|for|while)\(')

_FORBIDDEN_OPS = re.compile(r'[^a-zA-Z_]empty\(')
_KEYVALUE_BAD_OP = re.compile(r'([^|+<>!.* ]=|=[^ >\n]|=>[^ ])')

_FILE_EXT = re.compile(r'\.([a-z]+)$')


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
    line = _DOUBLE_QUOTES.sub('', line)
    # remove single quotes
    line = _SINGLE_QUOTES.sub('', line)
    return line


# removes JS-style regexps from code
def remove_js_regexps(line):
    line = _JS_REGEXPS.sub('', line)
    return line


# removes commas with HTML tags after them
def remove_commas_in_html(line):
    # remove cases like 'some words,<br/>'
    line = _HTML_COMMAS.sub('', line)
    return line


def remove_html_attributes(line):
    line = _RE_HTML_ATTRIBUTES.sub(' \\1"', line)
    return line


# convert all possible operators to one form
def convert_operators(line):
    line = line.replace('===', '=')
    line = line.replace('==', '=')
    return line


# removes bash arrays file{a,bc}
def remove_file_expansions(line):
    line = _FILE_EXPANSIONS.sub('', line)
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

        if 'nostyle' in line:
            continue

        # line endings check
        lem = _LINE_ENDINGS.match(line)
        if not lem:
            lem = _LINE_ENDINGS_LAST.match(line)
            # okay, last line may contain no CR-LF chars
            if not lem:
                bad_lines.add("UNIX-style line endings only allowed", index)

        # spaces count check
        sm = _SPACES.search(line)
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
        if '\t' in line:
            bad_lines.add("No tabs allowed", index)

        # shorttag check
        stm = _SHORTTAG.search(line)
        if not stm:
            stm = _SHORTTAG_SHORT.search(line)
        if stm:
            bad_lines.add("No PHP shorttags allowed", index)

        line_cleanup = line
        line_cleanup = remove_html_attributes(line_cleanup)
        line_cleanup = remove_strings(line_cleanup)
        line_cleanup = remove_js_regexps(line_cleanup)
        line_cleanup = remove_file_expansions(line_cleanup)
        line_cleanup = remove_commas_in_html(line_cleanup)
        line_cleanup = convert_operators(line_cleanup)
        line_cleanup = _COMMA_END.sub('', line_cleanup)

        # flow control operators ugly style check
        itm = _UGLY_CONTROL.search(line_cleanup)
        if itm:
            bad_lines.add("if/elseif/for/foreach/while clause should be separated from condition braces", index)

        # missing spaces after commas
        sac = _SPACES_COMMAS.search(line_cleanup)
        if sac:
            bad_lines.add("Commas should contain spaces after them", index)

        # trailing spaces check
        ts = _TRAILING_SPACES.search(line)
        if ts:
            bad_lines.add("No trailing spaces allowed", index)

        # forbidden PHP operators
        if file_type in common.PHP_FILES:
            empty_op = _FORBIDDEN_OPS.search(line)
            if empty_op:
                bad_lines.add("Operator 'empty' is forbidden for " + str(common.PHP_FILES) + " files", index)

            nsbe = _KEYVALUE_BAD_OP.search(line_cleanup)
            if nsbe:
                bad_lines.add("Assignment/comparison/key-value (=>) operators should be surrounded with spaces", index)

    print_bad_context(lines, bad_lines.lines())
    # return 1 if there some errors
    if len(bad_lines.lines()):
        return 1
    return 0


def check_file(name):
    lines = []
    ft_match = _FILE_EXT.search(name)
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

if 0:
    p = profile.Profile()
    p.run(textwrap.dedent(
        """
        for i in xrange(0, 20):
            check_file(sys.argv[1])
        """
    ))
    p.create_stats()
    p.print_stats(sort=1)

sys.exit(result)
