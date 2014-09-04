#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates test suite execution script
"""
import test_set_gen

imports, calls = test_set_gen.findTests(".", fileNamePrefix="xcms_", classNamePrefix="Xcms")
print test_set_gen.getHeader()
print test_set_gen.getFuncCode(imports, calls)
