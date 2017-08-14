#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import sys
import argparse
import logging
import collections

import selenium_test as st
import bawlib as bw
import test_set_gen

from pyvirtualdisplay import Display

# TODO(mvel): remove
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
""".format(script=os.path.basename(prog))


class TestSuiteError(Exception):
    pass


def print_stats(stats, detailed):
    if not stats:
        print "No tests were run"
        return

    detailed_od = collections.OrderedDict(sorted(detailed.items()))

    print "===== TEST SUITE DETAILED STATS: ====="
    for test_name, test_result in detailed_od.iteritems():
        print "  " + test_name + ": " + st.decode_run_result(test_result)

    print "===== TEST SUITE OVERALL STATS: ====="
    for test_result, testList in stats.iteritems():
        print st.decode_run_result(test_result) + ":", len(testList), "tests"


def generate_failed_tests_suite(failed_tests):
    # header
    imports = [file_name[:-3] for (file_name, _) in failed_tests]
    test_list = []
    for file_name, test_instance in failed_tests:
        full_test_name = test_instance.getName()
        module_name, class_name = full_test_name.split(".")
        test_list.append(test_set_gen.TestInfo(file_name, module_name, class_name))

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


_ENGINES = ["chrome", "firefox"]
_ENGINES_STR = ", ".join("'" + engine + "'" for engine in _ENGINES)


def parse_cmd_args():
    parser = argparse.ArgumentParser(description="Run test suite")
    parser.add_argument(
        "-t", "--test",
        type=str,
        default="",
        help="Run specific test",
    )

    parser.add_argument(
        "-s", "--test-set",
        type=str,
        default="",
        help="Specify test set to run (instead of default auto_test_set.py)",
    )

    parser.add_argument(
        "-u", "--url",
        type=str,
        default="fizlesh.local",
        help="Site to test (fizlesh.local by default)",
    )

    parser.add_argument(
        "-i", "--installer",
        default=False,
        action="store_true",
        help="Run installer test first",
    )

    parser.add_argument(
        "-l", "--list",
        default=False,
        action="store_true",
        help="List all tests in test set",
    )

    parser.add_argument(
        "-f", "--full-list",
        default=False,
        action="store_true",
        help="Print all tests in test set with descriptions",
    )

    parser.add_argument(
        "-b", "--break-on-errors",
        default=False,
        action="store_true",
        help="Break test suite on errors",
    )

    parser.add_argument(
        "-v", "--virtual",
        default=False,
        action="store_true",
        help="Use pyvirtualdisplay display (for headless runs)",
    )

    parser.add_argument(
        "-d", "--doc",
        default=False,
        action="store_true",
        help="Print test documentation",
    )

    parser.add_argument(
        "-e", "--engine",
        default="chrome",
        help="Browser engine to use. Valid options are: " + _ENGINES_STR + ", defaulting to " + _ENGINES[0],
    )

    parser.add_argument(
        "-p", "--profile-path",
        type=str,
        default=None,
        help="Use given browser profile path (firefox-only)",
    )

    return parser.parse_args()


def main():
    bw.configure_logger()

    args = parse_cmd_args()

    logging.info("Starting test suite")

    if args.installer:
        logging.info("We'll perform installer test first")

    if args.break_on_errors:
        logging.info("We'll break test suite on any test fail/fatal error")

    # last remaining argument is base test URL.

    if args.virtual:
        display = Display(visible=0, size=(1024, 768))
        display.start()

    if args.test:
        logging.info("We are going to run just one test named %s", args.test)

    if args.engine not in _ENGINES:
        logging.error("Invalid browser engine specified: '%s', valid are %s", args.engine, _ENGINES_STR)
        sys.exit(1)

    browser_holder = st.BrowserHolder(
        profile_path=args.profile_path,
        engine=args.engine,
    )

    base_url = args.url

    tests_module_name = "auto_test_set"

    if args.test_set:
        tests_module_name = args.test_set.replace(".py", "")

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

        tests = test_set_module.get_tests(base_url=base_url, browser_holder=browser_holder, args=args)

        # save installer test
        installer_test = None
        if tests:
            installer_test = tests.pop(0)

        failed_tests = []

        tests = [x for x in tests if test_match_filter(*x, testFilter=args.test)]
        if args.test and not tests:
            raise TestSuiteError("Specified test was not found in test suite. ")

        if args.installer:
            tests.insert(0, installer_test)

        # init detailed stats
        for (_file_name, test) in tests:
            test_detailed_stats[test.getName()] = None

        tests_done = 0
        tests_number = len(tests)

        while tests:
            file_name, test = tests.pop(0)
            if args.list:
                print file_name, test.getName()
            elif args.full_list:
                print "=" * 30
                print test.getName()
                print test.getDoc()
                print
            else:
                print "Running test {0} on site {1}".format(test.getName(), base_url)
                print test.getDoc()
                result = st.RunTest(test)
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
                if args.break_on_errors and result == 2:
                    print "Fatal error detected, stopping test suite."
                    break
                if args.break_on_errors and result == 1:
                    print "Test error detected, stopping test suite."
                    break

        # test loop end ------------------

        # fix #840: add rest of tests to failed, at the end of list.
        while tests:
            file_name, test = tests.pop(0)
            failed_tests.append((file_name, test))

        print_stats(test_stats, test_detailed_stats)
        generate_failed_tests_suite(failed_tests)

    except st.TestShutdown as exc:
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
