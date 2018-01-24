from flask_table import Table, Col
from flask import url_for, request


class EasyTable(Table):
    """
    Table class for sortable tables
    Now all columns are marked as sortable
    """

    allow_sort = True

    def __init__(self, *args, cols=(), **kwargs):
        """
        Creates and fills columns according to columns nicknames
        :param args: args for Table.__init__()
        :param cols: list of NamedColumn (see db.py), database entries ot list
        :param kwargs: kwargs for Table.__init__()
        """
        super().__init__(*args, **kwargs)
        for c in cols:
            self.add_column(c.key, Col(c.nick))

    def sort_url(self, col_key, reverse=False):  # TODO: figure out when reverse flag is triggered
        """
        Implements column sort
        :param col_key: real column name to which sort must be applied
        :param reverse: it never really triggers, but it is in signature
        :return: url with sort arguments
        """
        if request.args.get('direction', 'asc') == 'asc':
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('Greet', sort=col_key, direction=direction)  # TODO: remove 'Greet'