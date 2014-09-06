#!/usr/bin/env python
# -*- coding: utf-8 -*-

import freshdb_001_installer


def getTests(baseUrl, args):
    return [
        ("freshdb_001_installer.py", freshdb_001_installer.FreshDbInstaller(baseUrl, args)),
    ]
