#!/usr/bin/python
# -*- coding: utf8 -*-

from selenium_test import RunTest, TestShutdown, decode_run_result
import test_set_gen
import sys

from bawlib import getOption, getSingleOption, CliParamError, fileBaseName

sys.path.append(".")


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
    -h, --help             Display this help
    -i, --installer        Run installer test prior to all rest suite
    -l, --list             List all tests in test set
    -f, --full-list        List all tests in test set with descriptions
    -s, --set <set>        Specify test set to run (instead of default auto_test_set.py)
    -t, --test <test>      Run specific test instead of all suite
    -b, --break            Break test suite on errors

TEST OPTIONS could be test-dependent. Commonly supported options are:
    -p, --preserve         Leave browser window after test finish/fail
    -c, --chrome           Use Google Chrome browser instead of Firefox
    -d, --doc              Display test documentation
""".format(script=fileBaseName(prog))


class TestSuiteError(Exception):
    pass


def printStats(stats, detailed):
    if not stats:
        print "No tests were run"
        return

    print "===== TEST SUITE DETAILED STATS: ====="
    for testName, test_result in detailed.iteritems():
        print "  " + testName + ": " + decode_run_result(test_result)

    print "===== TEST SUITE OVERALL STATS: ====="
    for test_result, testList in stats.iteritems():
        print decode_run_result(test_result) + ":", len(testList), "tests"


def generateFailedTestsSuite(failed_tests):
    # header
    imports = [fn[:-3] for (fn, _) in failed_tests]
    testList = []
    for (fn, testClass) in failed_tests:
        modName = testClass.__module__
        clName = testClass.getName()
        testList.append((fn, modName, clName))

    failedSuite = test_set_gen.getHeader() + "\n" + test_set_gen.getFuncCode(imports, testList)

    with open("failed_test_set.py", "w") as fs:
        fs.write(failedSuite)


def testMatchFilter(file_name, test_instance, testFilter):
    # currently, filter is just a file name prefix
    if not testFilter:
        return True
    if testFilter.endswith(".py"):  # it is a filename
        if file_name != testFilter:
            return False
    else:  # it is like a test's class name
        if testFilter not in test_instance.getName():
            return False
    return True

args = sys.argv[1:]  # exclude program name

try:
    doInstallerTest, args = getSingleOption(["-i", "--installer"], args)
    if doInstallerTest:
        print "We'll perform installer test first. "

    specTest, args = getOption(["-t", "--test"], args)
    doShowHelp, args = getSingleOption(["-h", "--help"], args)
    testSet, args = getOption(["-s", "--set"], args)
    doList, args = getSingleOption(["-l", "--list"], args)
    doFullList, args = getSingleOption(["-f", "--full-list"], args)
    breakOnErrors, args = getSingleOption(["-b", "--break"], args)
    if breakOnErrors:
        print "We'll break test suite on any test fail/fatal error. "

    testArgs = [x for x in args if x.startswith("-")]
    restArgs = [x for x in args if not x.startswith("-")]

except CliParamError as e:
    print "Option syntax error: ", e
    showHelp()
    sys.exit(1)

# last remaining argument is base test URL.

if doShowHelp:
    showHelp()
    sys.exit(1)

if specTest:
    print "We are going to run just one test named like '" + specTest + "'. "

baseUrl = None
if restArgs:
    baseUrl = restArgs.pop(0)

if restArgs:
    print "Error: trailing parameters detected: ", restArgs
    showHelp()
    sys.exit(1)

setModuleName = "auto_test_set"

if testSet:
    setModuleName = testSet.replace(".py", "")

try:
    testStats = {}
    testDetailedStats = {}

    testSetModule = __import__(setModuleName, [])

    if not testSetModule.getTests:
        raise TestSuiteError("There is no 'getTests' function defined in specified test set. ")

    tests = testSetModule.getTests(baseUrl, testArgs)

    # save installer test
    installerTest = None
    if tests:
        installerTest = tests.pop(0)

    failedTests = []

    tests = [x for x in tests if testMatchFilter(*x, testFilter=specTest)]
    if specTest and not tests:
        raise TestSuiteError("Specified test was not found in test suite. ")

    if doInstallerTest:
        tests.insert(0, installerTest)

    # init detailed stats
    for (_file_name, test) in tests:
        testDetailedStats[test.getName()] = None

    testsDone = 0
    testsNumber = len(tests)

    while tests:
        fileName, test = tests.pop(0)
        if doList:
            print fileName, test.getName()
        elif doFullList:
            print "=" * 30
            print test.getName()
            print test.getDoc()
            print
        else:
            if not baseUrl:
                raise TestSuiteError("Test site URL not specified, cannot continue. ")

            print "Running test {0} on site {1}".format(test.getName(), baseUrl)
            print test.getDoc()
            result = RunTest(test)
            if result != 0:
                failedTests.append((fileName, test))

            if result not in testStats:  # add new list
                testStats[result] = [test.getName()]
            else:
                testStats[result].append(test.getName())

            testDetailedStats[test.getName()] = result

            testsDone += 1
            print "PROGRESS: Done {done} of {total} tests".format(done=testsDone, total=testsNumber)

            if result == 3:
                print "User interrupt, stopping test suite."
                break
            if breakOnErrors and result == 2:
                print "Fatal error detected, stopping test suite."
                break
            if breakOnErrors and result == 1:
                print "Test error detected, stopping test suite."
                break

    # test loop end ------------------

    # fix #840: add rest of tests to failed, at the end of list.
    while tests:
        fileName, test = tests.pop(0)
        failedTests.append((fileName, test))

    printStats(testStats, testDetailedStats)
    generateFailedTestsSuite(failedTests)

except TestShutdown as e:
    pass
except ImportError as e:
    print "Failed to load test set '" + setModuleName + "' as Python module. "
    print "Details: "
    print e
except TestSuiteError as e:
    print "TestSuiteError:", e
    sys.exit(2)
