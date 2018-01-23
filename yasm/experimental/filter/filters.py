from flask_table import Table, Col
from flask import url_for, request
import jinja2


def no_request_render_template(template_name, **context):
    """
    CRUTCH, now it hooks filter templates
    :param template_name: string
    :param context: dictionary
    :return: rendered template
    """
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('experimental.filter', 'templates')  # TODO: make template loader appropriate
    )                                                                    # Should we make our little template manager?
    template = env.get_template(template_name)
    return template.render(**context)


class FilterItem():
    """
    Single item in filter menu.
    """
    def __init__(self, cl):
        tp = cl.expression.type
        nick = cl.nick if cl.nick else cl.name
        if tp.__class__.__name__ == 'Enum':
            self.element = {'type': 'select', 'name': nick, 'options': tp.enums}
        elif tp.__class__.__name__ == 'Integer':
            self.element = {'type': 'number', 'name': nick}
        elif tp.__class__.__name__ == 'Text':
            self.element = {'type': 'text', 'name': nick}
        else:
            print(tp)

    def as_html(self):
        """
        converts item to html
        :return: html for this item
        """
        return no_request_render_template('element.html', data=self.element)


class EasyFilter():
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
        return no_request_render_template('filter.html', els=elements)
