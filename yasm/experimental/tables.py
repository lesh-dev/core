from flask_table import Table, Col
from flask import url_for, request

class EasyTable(Table):
    def __init__(self, *args, cols=(), **kwargs):
        super().__init__(*args, **kwargs)
        for c in cols:
            self.add_column(c.key, Col(c.nick))
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        if request.args.get('direction', 'asc') == 'asc':
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('Greet', sort=col_key, direction=direction)