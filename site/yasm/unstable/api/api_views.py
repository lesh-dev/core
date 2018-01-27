from flask import request
from sqlalchemy import or_
from flask.views import View
from flask_json import FlaskJSON, as_json
from json import loads
from checks import *


json = FlaskJSON()


class Api(View):
    @as_json
    def dispatch_request(self):
        def add_order(query, model, sort_dict):
            sort_direction = None
            sort_column = sort_dict['name']
            if 'direction' in sort_dict.keys():
                sort_direction = sort_dict['direction']

            sort_column = entities_by_entities_names(model, [sort_column])
            if sort_column is None:
                return query
            sort_column = sort_column[0]
            if sort_direction is None or sort_direction == 'asc':
                query = query.order_by(sort_column)
            elif sort_direction == 'desc':
                query = query.order_by(sort_column.desc())
            return query

        def add_filters(query, model, filter_list):
            def add_filter(query, model, filter_dict):
                filter_column = filter_dict['column']
                entity = entities_by_entities_names(model, [filter_column])
                if entity is None:
                    return query
                entity = entity[0]
                tp = entity.type.python_type
                inverse = filter_dict['not'] == "True"
                filter_type = filter_dict['type']
                if filter_type == 'isNone':
                    if inverse:
                        return query.filter(entity.isnot(None))
                    else:
                        return query.filter(entity.is_(None))
                if filter_type == 'is':
                    value = tp(filter_dict['value'])
                    if inverse:
                        return query.filter(entity.isnot(value))
                    else:
                        return query.filter(entity.is_(value))
                if filter_type == 'range':
                    v1 = tp(filter_dict['value']['lower'])
                    v2 = tp(filter_dict['value']['upper'])
                    if inverse:
                        return query.filter(or_(v1 > entity, entity >= v2))
                    else:
                        return query.filter(v1 <= entity, entity < v2)
                if filter_type == 'greater':
                    value = tp(filter_dict['value'])
                    if inverse:
                        return query.filter(entity <= value)
                    else:
                        return query.filter(entity > value)
                if filter_type == 'less':
                    value = tp(filter_dict['value'])
                    if inverse:
                        return query.filter(entity >= value)
                    else:
                        return query.filter(entity < value)
                if filter_type == 'eq':
                    value = tp(filter_dict['value'])
                    if inverse:
                        return query.filter(entity != value)
                    else:
                        return query.filter(entity == value)
            for filt in filter_list:
                query = add_filter(query, model, filt)
            return query

        quest = loads(request.args.get('request', None))
        table = quest['table']
        nicks = quest['entities'].keys()
        entities_names = quest['entities'].values()
        model = model_by_table_name(table)
        ret = []
        if model:
            entities = entities_by_entities_names(model, entities_names)
            if entities:
                query = model.query.with_entities(*entities)

                if 'sort' in quest.keys():
                    query = add_order(query, model, quest['sort'])

                if 'filter' in quest.keys():
                    query = add_filters(query, model, quest['filter'])

                for row in query.all():
                    ret.append(dict(zip(nicks, row)))
        return {'results': ret}
