# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired


class DynTableForm(Form):
    id_ = StringField('Table Name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def from_model(self, table):
        self.id_.data = table.id

    def to_model(self, table):
        table.set_id(self.id_.data)


class DynAttributeForm(Form):
    attr_name = StringField('Attribute Name', validators=[DataRequired()])
    pk = BooleanField('Primary Key')
    display = StringField('Display', validators=[DataRequired()])
    attr_type = SelectField(u'Type', choices=[('IntegerField', 'Integer Field'),
                 ('StringField', 'String Field'), \
                 ('BooleanField', 'Boolean Field')])
    required = BooleanField('Required')
