from flask import request
from sqlalchemy import or_
from flask.views import View
from flask_json import FlaskJSON, as_json
from json import loads
from checks import *


json = FlaskJSON()


class Api(View):
    """
    This implements the api view see dispatch_request docs
    """
    @as_json
    def dispatch_request(self):
        """
        :arg: there are no straight arguments, but flask.request is set
        flask.request should contain argument 'request', which is a JSON packed dictionary
        :parameter: flak.request['request'] is a dictionary with structure: {
            "table":<table to select from>,
            "entities": {
                "<column nickname (how it would be called in response)>":"<column name as in schema>"
            },
            "sort": <sort_dict> (see add_order doc),
            "filter": <filter_list> (see add_filters doc)
        }
        :return: dictionary {'results': results} which is translated to JSON with decorator
        """
        def add_order(query, model, sort_dict):
            """
            adds order_by method to query
            :param query: already existing query
            :param model: any model from db.py
            :param sort_dict: dictionary: {
                "column": <column name as in schema>,
                "direction": <"asc" or "desc" or omitted>
            }
            :return: query with added order
            """
            sort_direction = None
            sort_column = sort_dict['column']
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
            """
            adds filters to query
            :param query: already existing query
            :param model: any model from db.py
            :param filter_list: list [
                <filter_dict>, ...
            ]
            :return: query with added filters
            """
            def add_filter(query, model, filter_dict):
                """
                adds single filter to query
                :param query: already existing query
                :param model: any model from db.py
                :param filter_list: dictionary: {
                    "column": <column name as in schema>,
                    "type": <"eq", "isNone", "is", "less", "greater", "range">,
                    "not": <"True", "False"> (inverting query)
                    "values": specific values for query type
                }
                :return: query with added filter
                """
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
