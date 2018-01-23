from flask.views import View
from flask import request
from yasm.experimental import tables
from yasm.experimental.filter.filters import EasyFilter

from yasm.db import Person, PersonSchool


class Test(View):
    def dispatch_request(self):
        sort = request.args.get('sort', '')
        reverse = (request.args.get('direction', 'asc') == 'desc')
        p = tables.EasyTable(Person.query.order_by(sort + " desc" * reverse).all(), cols=[
            Person.person_id,
            Person.first_name,
            Person.last_name,
            Person.patronymic
        ])
        filter = EasyFilter([
            PersonSchool.curatorship,
            PersonSchool.person_school_changedby,
            PersonSchool.school_id
        ])
        print(len(filter.items))
        return filter.as_html() + p.__html__()
