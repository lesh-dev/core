from flask import request
from flask.views import View

from db import Person, PersonComment
from unstable.filter.filters import EasyFilter
import unstable.table as table


class Test(View):
    def dispatch_request(self):
        sort = request.args.get('sort', '')
        reverse = (request.args.get('direction', 'asc') == 'desc')
        p = table.easy_table('Persons', cols=[
            Person.person_id,
            Person.first_name,
            Person.last_name,
            Person.patronymic
        ])
        p = p(Person.query.order_by(sort + " desc" * reverse).all())

        filter = EasyFilter([
            PersonComment.blamed_person_id,
            PersonComment.school_id
        ])

        return filter.as_html() + p.no_head_html()
