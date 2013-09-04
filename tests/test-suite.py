#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium_test import RunTest, TestShutdown, DecodeRunResult
import test_xcms_installer
import sys

from bawlib import getOption, getSingleOption, isVoid, CliParamError, fileBaseName

def showHelp():
    prog = sys.argv[0]
    print """
Syntax: {script} [OPTIONS] [TEST OPTIONS] <site-url>
Most generic usage:
  {script} [-i] [TEST OPTIONS] <site-url>
  This command runs default test set 'auto_test_set.py'
Run specific test:
  {script} -t <test-name> [TEST OPTIONS] <site-url>
List test in test set (or list tests with full descriptions):
  {script} -l(-f) <test-name>

Examples:
  {script} test.fizlesh.ru
  {script} -t XcmsXsmAnketaFill test.fizlesh.ru
  {script} -t xcms_xsm_anketa_fill.py test.fizlesh.ru

ALL OPTIONS:
  -h, --help\t\tDisplay this help
  -i, --installer\tRun installer test prior to all rest suite
  -t, --test <test>\tRun specific test instead of all suite
  -l, --list\t\tList all tests in test set
  -f, --full-list\t\tList all tests in test set with descriptions
  -s, --set\t\tSpecify test set to run (instead of default auto_test_set.py)
  -b, --break\t\tBreak test suite running on fatal errors

TEST OPTIONS could be test-dependent. Commonly supported options are: 
  -p, --preserve\tLeave browser window after test finish/fail
  -d, --doc\t\tDisplay test documentation
""".format(script = fileBaseName(sys.argv[0]))


def printStats(stats):
    if not stats:
        print "No tests were run"
        return
    print "Run overall statistics:"
    for result, testList in stats.iteritems():
        print DecodeRunResult(result) + ":", len(testList),"tests"
    
args = sys.argv[1:] # exclude program name

try:
    doInstallerTest, args = getSingleOption(["-i", "--installer"], args)

    specTest, args = getOption(["-t", "--test"], args)
    doShowHelp, args = getSingleOption(["-h", "--help"], args)
    testSet, args = getOption(["-s", "--set"], args)
    doList, args = getSingleOption(["-l", "--list"], args)
    doFullList, args = getSingleOption(["-f", "--full-list"], args)
    breakOnFatals, args = getSingleOption(["-b", "--break"], args)
    
except CliParamError as e:
    print "Option syntax error: ", e
    showHelp()
    sys.exit(1)
    
# last remaining argument is base test URL.

if doShowHelp:
    showHelp()
    sys.exit(1)

if specTest:
    print "We are going to run just one test " + specTest + ". "

baseUrl = None
if len(args) >= 1:
    baseUrl = args.pop()
    if isVoid(baseUrl):
        showHelp()
        sys.exit(1)
else:
    if not (doList or doFullList):
        print "Test site URL not defined. "
        showHelp()
        sys.exit(1)

if doInstallerTest:
    print "Running installer test. "
    RunTest(test_xcms_installer.TestXcmsInstaller(baseUrl, args))
 
setModuleName = "auto_test_set"

if testSet:
    setModuleName = testSet.replace(".py", "")

try:
    testStats = {}
    
    testSetModule = __import__(setModuleName, [])   
    
    if not testSetModule.getTests:
        print "There is no 'getTests' function defined in specified test set. "
        sys.exit(1)
        
    tests = testSetModule.getTests(baseUrl, args)
    specTestFound = False
    while tests:
        fileName, test = tests.popitem()
        if specTest:
            if specTest.endswith(".py"): # it is a filename
                if fileName != specTest:
                    continue
            else: # it is a test class name
                if test.getName() != specTest:
                    continue
        if doList:
            print fileName, test.getName()
        elif doFullList:
            print "=" * 30;
            print test.getName()
            print test.getDoc()
            print;
        else:
            if specTest:
                specTestFound = True
            print "Running test", test.getName(), "on site", baseUrl
            print test.getDoc()
            result = RunTest(test)
            if breakOnFatals and result == 2:
                print "Fatal error detected, stopping test suite."
                break
                
            if result not in testStats: # add new list
                testStats[result] = [test.getName()]
            else:
                testStats[result].append(test.getName())
    
    if specTest and not specTestFound:
        print "Specified test was not found in test suite. "
        
    printStats(testStats)

except TestShutdown as e:
    pass
except ImportError as e:
    print "Failed to load test set '" + setModuleName + "' as Python module. "
    print "Details: "
    print e

