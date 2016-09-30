#!/usr/bin/python

"""
Stupid code style fixer.
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


def fix_code_style(lines, file_type):
    fixed_lines = []
    for line in lines:
        if file_type in PHP_FILES:
            if 'foreach' in line and re.match(r'([^ ]=>|=>[^ ])', line):
                line = line.replace('=>', ' => ')
                line = line.replace('  ', ' ')

            line = re.sub(r'([\'"a-z])=>([\'"$A-Z])', '\\1 => \\2', line)

        fixed_lines.append(line)

    return fixed_lines


def fix_file(name):
    lines = []
    ft_match = re.search('\.([a-z]+)$', name)
    file_type = 'unknown'
    if ft_match:
        file_type = ft_match.group(1)
    with open(name) as f:
        for line in f:
            lines.append(line)

    fixed_lines = fix_code_style(lines, file_type)
    with open(name, 'w') as f:
        for line in fixed_lines:
            f.write(line)


def print_usage():
    print "Syntax: " + sys.argv[0] + " <file-name-to-fix>"
    sys.exit(1)


if len(sys.argv) < 2:
    print_usage()

try:
    fix_file(sys.argv[1])
except Exception as e:
    print 'ERROR', str(e)
    sys.exit(1)
