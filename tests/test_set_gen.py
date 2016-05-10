#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates test suite execution script
"""

import re
from os import listdir
from os.path import isfile

def getHeader():
    return """#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is auto-generated
"""

def getFuncCode(imports, testList):
    tab = ' ' * 4
    result = []
    for i in imports:
        result.append("import {0}".format(i))

    # respect pep8 code style - add 2 empty lines
    result += ["", ""]
    
    result.append('def getTests(baseUrl, args):')
    result.append(tab + 'return [')
    for testInfo in testList:
        result.append(tab * 2 + genOneTestLine(testInfo))
    result.append(tab + ']')
    return "\n".join(result)


def genOneTestLine(testInfo):
    (testFile, modName, clName) = testInfo
    return '("{testFile}", {modName}.{clName}(baseUrl, args)),'.format(testFile=testFile, modName=modName, clName=clName)


def findTests(directory='.', fileNamePrefix="xcms_", classNamePrefix="Xcms"):
    pyFiles = sorted([f for f in listdir(directory) if isfile(f) and f.startswith(fileNamePrefix) and f.endswith('.py')])

    test_set = set([])

    imports = []
    testList = []

    for fn in pyFiles:
        moduleName = fn[:-3]
        matchLine = "class " + classNamePrefix
        classLineList = [line for line in open(fn, 'r') if matchLine in line]
        if not classLineList:
            continue
        classLine = classLineList.pop().strip()
        r = re.match(r"class ([\w_]+)\([\w_.]+\):", classLine)
        if not r:
            #print "Cannot match in ", cl
            continue
        className = r.group(1)
        test_pair = (moduleName, className)
        if test_pair in test_set:
            raise Exception("Duplicate test: {}.{}", moduleName, className)
        test_set.add(test_pair)

        imports.append(moduleName)
        testList.append((fn, moduleName, className))
    return imports, testList

