#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates test suite execution script
"""

import logging
import re
import os


def get_header():
    return """#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is auto-generated
"""


class TestInfo(object):
    def __init__(self, file_name, module_name, class_name):
        self.file_name = file_name
        self.module_name = module_name
        self.class_name = class_name

    def key(self):
        return self.module_name, self.class_name

    def __hash__(self):
        return hash(self.key())

    def __cmp__(self, other):
        return cmp(self.key(), other.key())


def get_func_code(imports, test_list):
    tab = ' ' * 4
    result = []
    for i in imports:
        result.append("import {0}".format(i))

    # respect pep8 code style - add 2 empty lines
    result += ["", ""]

    result.append('def get_tests(**kwargs):')
    result.append(tab + 'return [')
    for testInfo in sorted(test_list):
        result.append(tab * 2 + gen_one_test_line(testInfo))
    result.append(tab + ']')
    return "\n".join(result)


def gen_one_test_line(test_info):
    """
    :type test_info: TestInfo
    :rtype: str
    """
    return '("{}", {}.{}(**kwargs)),'.format(test_info.file_name,
                                             test_info.module_name,
                                             test_info.class_name)


def find_tests(directory='.', file_name_prefix="xcms_", class_name_prefix="Xcms"):
    py_files = sorted([f for f in os.listdir(directory)
                       if os.path.isfile(f) and f.startswith(file_name_prefix) and f.endswith('.py')])

    logging.info("Found %s python files", len(py_files))

    test_set = set([])

    imports = []

    for file_name in py_files:
        module_name = file_name[:-3]
        match_line = "class " + class_name_prefix
        class_line_list = [line for line in open(file_name, 'r') if match_line in line]
        # first, simply exclude by primitive pattern 'class Xcms'
        if not class_line_list:
            continue
        class_decl_line = class_line_list.pop().strip()
        r = re.match(r"class ([\w_]+)\([\w_.]+\):", class_decl_line)
        if not r:
            continue
        class_name = r.group(1)
        test_info = TestInfo(file_name, module_name, class_name)
        if test_info in test_set:
            raise Exception("Duplicate test found: {}.{}", module_name, class_name)
        test_set.add(test_info)
        imports.append(module_name)
    return imports, list(test_set)
