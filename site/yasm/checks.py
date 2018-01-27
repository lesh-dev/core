import db


def check_table_name(tablename):
    return tablename in db.database.metadata.tables.keys()


def check_entities(tablename, entities):
    possible = [element.key for element in db.database.metadata.tables[tablename].columns._all_columns]
    for entity in entities:
        if entity not in possible:
            return False
    return True


def model_by_table_name(tablename):
    for model in db.registered_models:
        if model.__tablename__ == tablename:
            return model
    return None


def entities_by_entities_names(model, entitiesname):
    d = model._sa_class_manager
    keys = d.keys()
    ret = []
    for entity in entitiesname:
        if entity not in keys:
            return None
        else:
            ret.append(d[entity])
    return ret