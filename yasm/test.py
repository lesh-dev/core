from flask.views import View
from flask import request
from yasm.experimental import tables

from yasm.db import Person


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
        print(Person.person_id.__dict__)
        return p.__html__()
