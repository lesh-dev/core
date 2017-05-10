#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import logging
import collections

from selenium_test import RunTest, TestShutdown, BrowserHolder, decode_run_result
import test_set_gen
from test_set_gen import TestInfo

from bawlib import getOption, getSingleOption, CliParamError, fileBaseName
from bawlib import configure_logger

from pyvirtualdisplay import Display

# TODO: remove
import auto_test_set

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
    -h, --help                Display this help
    -i, --installer           Run installer test prior to all rest suite
    -l, --list                List all tests in test set
    -f, --full-list           List all tests in test set with descriptions
    -s, --set <set>           Specify test set to run (instead of default auto_test_set.py)
    -t, --test <test>         Run specific test instead of all suite
    -b, --break               Break test suite on errors
    -p, --profile-path <path> Use given browser profile path (firefox only)
    -v, --virtual             Uses pyvirtualdisplay display

TEST OPTIONS could be test-dependent. Commonly supported options are:
    -c, --chrome           Use Google Chrome browser instead of Firefox
    -d, --doc              Display test documentation
""".format(script=fileBaseName(prog))


class TestSuiteError(Exception):
    pass


def print_stats(stats, detailed):
    if not stats:
        print "No tests were run"
        return

    detailed_od = collections.OrderedDict(sorted(detailed.items()))

    print "===== TEST SUITE DETAILED STATS: ====="
    for test_name, test_result in detailed_od.iteritems():
        print "  " + test_name + ": " + decode_run_result(test_result)

    print "===== TEST SUITE OVERALL STATS: ====="
    for test_result, testList in stats.iteritems():
        print decode_run_result(test_result) + ":", len(testList), "tests"


def generate_failed_tests_suite(failed_tests):
    # header
    imports = [file_name[:-3] for (file_name, _) in failed_tests]
    test_list = []
    for file_name, test_instance in failed_tests:
        full_test_name = test_instance.getName()
        module_name, class_name = full_test_name.split(".")
        test_list.append(TestInfo(file_name, module_name, class_name))

    failed_suite = test_set_gen.get_header() + "\n" + test_set_gen.get_func_code(imports, test_list)

    with open("failed_test_set.py", "w") as fs:
        fs.write(failed_suite)


def test_match_filter(file_name, test_instance, testFilter):
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


def main():
    configure_logger()

    args = sys.argv[1:]  # exclude program name

    logging.info("Starting test suite")
    try:
        doInstallerTest, args = getSingleOption(["-i", "--installer"], args)
        if doInstallerTest:
            print "We'll perform installer test first. "

        specTest, args = getOption(["-t", "--test"], args)
        profile_path, args = getOption(["-p", "--profile-path"], args)
        doShowHelp, args = getSingleOption(["-h", "--help"], args)
        testSet, args = getOption(["-s", "--set"], args)
        doList, args = getSingleOption(["-l", "--list"], args)
        doFullList, args = getSingleOption(["-f", "--full-list"], args)
        breakOnErrors, args = getSingleOption(["-b", "--break"], args)
        runVirtualDisplay, args = getSingleOption(["-v", "--virtual"], args)
        if breakOnErrors:
            print "We'll break test suite on any test fail/fatal error. "

        test_args = [x for x in args if x.startswith("-")]
        rest_args = [x for x in args if not x.startswith("-")]

    except CliParamError as exc:
        print "Option syntax error: ", exc
        showHelp()
        sys.exit(1)

    # last remaining argument is base test URL.

    if runVirtualDisplay:
        display = Display(visible=0, size=(1024, 768))
        display.start()

    if doShowHelp:
        showHelp()
        sys.exit(1)

    if specTest:
        print "We are going to run just one test named like '" + specTest + "'. "

    browser_holder = BrowserHolder(profile_path=profile_path)

    base_url = None
    if rest_args:
        base_url = rest_args.pop(0)

    if rest_args:
        print "Error: trailing parameters detected: ", rest_args
        showHelp()
        sys.exit(1)

    tests_module_name = "auto_test_set"

    if testSet:
        tests_module_name = testSet.replace(".py", "")

    try:
        test_stats = {}
        test_detailed_stats = {}

        test_set_module = __import__(tests_module_name, [])

        if not test_set_module.get_tests:
            raise TestSuiteError("There is no 'getTests' function defined in specified test set. ")

        # FIXME(vdmit): Find proper way to deal with it
        # this is not necessary for tests listing
        # but `get_tests` expects base_url is not None
        if not base_url:
            raise TestSuiteError("Test site URL not specified, cannot continue. ")

        tests = test_set_module.get_tests(base_url=base_url, browser_holder=browser_holder, params=test_args)

        # save installer test
        installer_test = None
        if tests:
            installer_test = tests.pop(0)

        failed_tests = []

        tests = [x for x in tests if test_match_filter(*x, testFilter=specTest)]
        if specTest and not tests:
            raise TestSuiteError("Specified test was not found in test suite. ")

        if doInstallerTest:
            tests.insert(0, installer_test)

        # init detailed stats
        for (_file_name, test) in tests:
            test_detailed_stats[test.getName()] = None

        tests_done = 0
        tests_number = len(tests)

        while tests:
            file_name, test = tests.pop(0)
            if doList:
                print file_name, test.getName()
            elif doFullList:
                print "=" * 30
                print test.getName()
                print test.getDoc()
                print
            else:
                print "Running test {0} on site {1}".format(test.getName(), base_url)
                print test.getDoc()
                result = RunTest(test)
                if result != 0:
                    failed_tests.append((file_name, test))

                if result not in test_stats:  # add new list
                    test_stats[result] = [test.getName()]
                else:
                    test_stats[result].append(test.getName())

                test_detailed_stats[test.getName()] = result

                tests_done += 1
                logging.info("PROGRESS: Done %s of %s tests, %s failed", tests_done, tests_number, len(failed_tests))

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
            file_name, test = tests.pop(0)
            failed_tests.append((file_name, test))

        print_stats(test_stats, test_detailed_stats)
        generate_failed_tests_suite(failed_tests)

    except TestShutdown as exc:
        logging.debug("Got test shutdown: %s", exc)
        pass
    except ImportError as exc:
        print "Failed to load test set '" + tests_module_name + "' as Python module. "
        print "Details: "
        print exc
    except TestSuiteError as exc:
        print "TestSuiteError:", exc
        sys.exit(2)


if __name__ == "__main__":
    main()
