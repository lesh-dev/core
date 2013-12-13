#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates test suite execution script
"""

import re
from os import listdir
from os.path import isfile

py_files = sorted([ f for f in listdir('.') if isfile(f) and f[-3:] == '.py' ])

imports = []
calls = []

for fn in py_files:
    moduleName = fn[:-3]

    classLineList = [line for line in open(fn, 'r') if "class Xcms" in line]
    if not classLineList:
        continue
    classLine = classLineList.pop().strip()
    r = re.match(r"class ([\w]+)\([\w_.]+Test\):", classLine)
    if not r:
        #print "Cannot match in ", cl
        continue

    imports.append(moduleName)
    calls.append( '"%s": %s.%s(baseUrl, args),' % (fn, moduleName, r.group(1)))

print '#!/usr/bin/env python'
print '# -*- coding: utf-8 -*-'
print '"""'
print "This file is AUTO-GENERATED"
print "Do not edit it, fix generator instead"
print '"""'
print
for i in imports:
    print 'import', i
print

print 'def getTests(baseUrl, args): return {'
for i in calls:
    print '    ' + i
print '}'
