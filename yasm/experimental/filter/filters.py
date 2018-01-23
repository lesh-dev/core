from flask_table import Table, Col
from flask import url_for, request


class FilterItem():
    def __init__(self, cl):
        tp = cl.expression.type
        nick = cl.nick if cl.nick else cl.name
        if tp.__class__.__name__ == 'Enum':
            self.element = ('enum', nick, tp.enums)
        elif tp.__class__.__name__ == 'Integer':
            self.element = ('int', nick)
        elif tp.__class__.__name__ == 'Text':
            self.element = ('int', nick)

    def as_html(self):
        pass


class EasyFilter():
    cols = []

    def __init__(self, cols=()):
        for c in cols:
            self.cols.append(FilterItem(c))

    def as_html(self):
        pass