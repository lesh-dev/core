#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates test suite execution script
"""

import logging
import test_set_gen
import bawlib


def main():
    bawlib.configure_logger()
    logging.info("Generating test set")
    imports, calls = test_set_gen.find_tests(".", file_name_prefix="xcms_", class_name_prefix="Xcms")
    print test_set_gen.get_header()
    print test_set_gen.get_func_code(imports, calls)
    logging.info("Done")


if __name__ == "__main__":
    main()
