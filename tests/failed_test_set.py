#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is auto-generated

import xcms_auth_forgot_password


def getTests(baseUrl, args):
    return {
        "xcms_auth_forgot_password.py": xcms_auth_forgot_password.XcmsAuthForgotPassword(baseUrl, args),
    }