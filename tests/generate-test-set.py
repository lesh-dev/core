#!/usr/bin/python

import re
from os import listdir
from os.path import isfile, join

pyFiles = sorted([ f for f in listdir('.') if isfile(f) and f[-3:] == '.py' ])

imp = []
main = []

for fn in pyFiles:
	moduleName = fn[:-3]

	classLineList = filter(lambda x: "class Xcms" in x, [line for line in open(fn, 'r')])
	if not classLineList:
		continue
	classLine = classLineList.pop().strip()
	r = re.match("class ([\w]+)\(SeleniumTest\):", classLine)
	if not r:
		#print "Cannot match in ", cl
		continue

	imp.append(moduleName)
	main.append( '"%s": %s.%s(baseUrl, args),' % (fn, moduleName, r.group(1)))

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
