from extensions import db
from sqlalchemy.ext.automap import automap_base

classes = {}

def load_class(name):
    name = name.lower()
    if name not in classes:
        db.Model.metadata.reflect(db.engine)
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        classes[name] = Base.classes.get(name)
    return classes[name]

def create_table(table_name, attributes=[]):
    methods = {}
    methods['__tablename__'] = table_name.lower()
    for attr in attributes:
        attr_type = ret_type(attr.get('attr_type')[0])
        if attr.get('pk'):
            methods[str(attr.get('attr_name').lower())] = db.Column(attr_type,
                primary_key=True)
        else:
            methods[str(attr.get('attr_name').lower())] = db.Column(attr_type)
    table = type(str(table_name), (db.Model, ), methods)
    return table


def ret_type(char):
    type_ = db.Integer
    if char == 'S':
        type_ = db.String
    elif char == 'B':
        type_ = db.Boolean
    return type_


def drop_table(table_name):
    load_class(table_name).__table__.drop(db.engine, checkfirst=True)
