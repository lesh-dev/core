#!/usr/bin/python

import re
from os import listdir
from os.path import isfile, join

py_files = [ f for f in listdir('.') if isfile(f) and f[-3:] == '.py' ]

imp = []
main = []

for fn in py_files:
    fnc = fn[:-3]

    cl = ''
    for l in open(fn, 'r'):
        if 'class Xcms' in l:
            cl = l
            break
    cl = cl.strip()
    r = re.match("class ([A-Za-z]+)\(SeleniumTest\):", cl)
    if not r:
        #print "Cannot match in ", cl
        continue

    imp.append(fnc)
    main.append( '"%s": %s.%s(baseUrl, args),' % (fn, fnc, r.group(1)))

print '#!/usr/bin/python'
print
print "# This file is AUTO-GENERATED. Do not edit it directly, edit generator instead"
print
for i in imp:
    print 'import', i
print

print 'def getTests(baseUrl, args): return {'
for i in main:
    print '    ' + i
print '}'
