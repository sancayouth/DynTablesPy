# -*- coding: utf-8 -*-
from app import db
from sqlalchemy.ext.declarative import declarative_base


class DynTable(db.Model):

    __tablename__ = 'dyntables'

    id = db.Column(db.String, primary_key=True)
    attributes = db.relationship('DynAttribute',
                                     backref=db.backref('owner'),
                                     cascade='all, delete')

    def __init__(self, name):
        self.id = name.lower().replace(' ', '_')

    def set_id(self, id):
        self.id = id.lower().replace(' ', '_')

    def __repr__(self):
        return '<DynTable (table_name=%r)>' % (self.id)


class DynAttribute(db.Model):

    __tablename__ = 'dynattributes'

    id = db.Column(db.String, primary_key=True)
    pk = db.Column(db.Boolean)
    dyntable_id = db.Column(db.String, db.ForeignKey('dyntables.id'))
    attr_name = db.Column(db.String)
    display = db.Column(db.String)
    attr_type = db.Column(db.String(1))
    required = db.Column(db.Boolean)

    def __init__(self, name, dynt_id, display,
                 attr_t, pk=False, required=False):
        self.id = dynt_id + ':' + name.lower().replace(' ', '_')
        self.attr_name = name.lower().replace(' ', '_')
        self.pk = pk
        self.dyntable_id = dynt_id
        self.display = display
        self.attr_type = attr_t
        self.required = required

    def __repr__(self):
        return '<DynAttribute (attribute_name=%r)>' % (self.id)


def create_table(table_name, attributes=[]):
    methods = {}
    methods['__tablename__'] = table_name
    for attr in attributes:
        attr_type = ret_type(attr.get('attr_type'))
        if attr.get('pk'):
            methods[str(attr.get('attr_name'))] = db.Column(attr_type,
                primary_key=True)
        else:
            methods[str(attr.get('attr_name'))] = db.Column(attr_type)
    table = type(str(table_name), (db.Model, ), methods)
    return table


def ret_type(char):
    type_ = db.Integer
    if char == 'S':
        type_ = db.String
    elif char == 'B':
        type_ = db.Boolean
    return type_
