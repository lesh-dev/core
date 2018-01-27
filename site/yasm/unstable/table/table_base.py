from flask_table import Table, Col, create_table
from flask_table.html import element
from flask import url_for, request
import types
import re


def no_head_html(self):
    tbody = self.tbody()
    if tbody or self.allow_empty:
        content = '\n{tbody}\n'.format(
            tbody=tbody,
        )
        return element(
            'table',
            attrs=self.get_html_attrs(),
            content=content,
            escape_content=False)
    else:
        return element('p', content=self.no_items)


def html(self):
    tbody = self.tbody()
    if tbody or self.allow_empty:
        content = '\n{thead}\n{tbody}\n'.format(
            thead=self.thead(),
            tbody=tbody,
        )
        return element(
            'table',
            attrs=self.get_html_attrs(),
            content=content,
            escape_content=False)
    else:
        return element('p', content=self.no_items)


def easy_table(name='Table', cols=()):
    tbl = create_table(name)
    for c in cols:
        tbl.add_column(c.key, Col(c.nick))
    tbl.no_head_html = no_head_html
    tbl.html = html
    return tbl