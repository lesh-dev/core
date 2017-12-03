#!/usr/bin/python
# -*- coding: utf8 -*-

import random_crap


class Page(object):
    """
        Simple page operating object
    """
    def __init__(self, xtest):
        self.xtest = xtest
        self.page_dir = None
        self.menu_title = None
        self.header = None
        self.alias = None

    def input(
        self,
        page_dir=None,
        menu_title=None,
        header=None,
        alias=None,
        permissions=[],
        random=False,
    ):
        t = self.xtest
        if page_dir is not None:
            if random:
                page_dir += random_crap.random_text(8)
            self.page_dir = t.fillElementById("create-name-input", page_dir)

        if menu_title is not None:
            if random:
                menu_title += random_crap.random_text(8)
            self.menu_title = t.fillElementById("menu-title-input", menu_title)

        if header is not None:
            if random:
                header += random_crap.random_text(8)
            self.header = t.fillElementById("header-input", header)

        if alias is not None:
            if random:
                alias += random_crap.random_text(8)
            alias = t.fillElementById("alias-input", alias)

        default_page_type = t.getOptionValueById("create-pagetype-selector")

        if default_page_type != "content":
            t.failTest("Default selected page type is not 'content': " + default_page_type)

        # default values
        self.assertCheckboxValueById("view_#all-checkbox", True)
        self.assertCheckboxValueById("view_#registered-checkbox", False)

        for permission in permissions:
            self.clickElementById("{}-checkbox".format(permission))

        t.clickElementById("create-page-submit")
