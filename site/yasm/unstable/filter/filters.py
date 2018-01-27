from flask_table import Table, Col
from flask import url_for, request
from unstable.template_loader import no_request_render_template
from .display_tables import get_display


class FilterItem:
    """
    Single item in filter menu.
    """
    def __init__(self, cl):
        fk_set = cl.foreign_keys
        nick = cl.nick if cl.nick else cl.name
        if len(fk_set) == 0:
            tp = cl.expression.type
            if tp.__class__.__name__ == 'Enum':
                self.element = {'type': 'select', 'name': nick, 'options': tp.enums}
            elif tp.__class__.__name__ == 'Integer':
                self.element = {'type': 'number', 'name': nick}
            elif tp.__class__.__name__ == 'Text':
                self.element = {'type': 'text', 'name': nick}
            else:
                print(tp)
        else:
            ref_cl = list(fk_set)[0].referenced_model.class_  # is this really the only way?
            options = get_display(ref_cl)

            self.element = {'type': 'select', 'name': nick, 'options': options}  # TODO:...

    def as_html(self):
        """
        converts item to html
        :return: html for this item
        """
        return no_request_render_template('unstable/filter/templates', 'element.html', data=self.element)


class EasyFilter:
    def __init__(self, cols=()):
        self.items = []
        for c in cols:
            self.items.append(FilterItem(c))

    def as_html(self):
        """
        builds filter html
        :return: rendered template
        """
        elements = list(map(lambda x: x.as_html(), self.items))
        return no_request_render_template('unstable/filter/templates', 'filter.html', els=elements)
