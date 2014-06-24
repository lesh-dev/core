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

def getFuncCode(imports, testMap):
    tab = ' ' * 4
    result = []
    for i in imports:
        result.append("import {0}".format(i))

    # respect pep8 code style
    result += ["", ""]
    
    result.append('def getTests(baseUrl, args):')
    result.append(tab + 'return {')
    for i in testMap:
        result.append(tab * 2 + i)
    result.append(tab + '}')
    return "\n".join(result)

def findTests(directory):
    py_files = sorted([ f for f in listdir('.') if isfile(f) and f[0:5] == "xcms_" and f[-3:] == '.py' ])

    imports = []
    testMap = []

    for fn in py_files:
        moduleName = fn[:-3]

        classLineList = [line for line in open(fn, 'r') if "class Xcms" in line]
        if not classLineList:
            continue
        classLine = classLineList.pop().strip()
        r = re.match(r"class ([\w_]+)\([\w_.]+\):", classLine)
        if not r:
            #print "Cannot match in ", cl
            continue
        className = r.group(1)

        imports.append(moduleName)
        testMap.append('"{testFile}": {modName}.{clName}(baseUrl, args),'.format(testFile=fn, modName=moduleName, clName=className))
    return imports, testMap
