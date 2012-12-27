## it's the template part of auto-generated script.
## used to create test-suite.py
				
while len(tests) > 0:
	test = tests.pop()
	if specTest and test.getName() != specTest: continue
	print test.getDoc()
	RunTest(test)


