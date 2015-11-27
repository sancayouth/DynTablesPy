# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DynTableForm(Form):
    id_ = StringField('Table Name', validators=[DataRequired()])
    submit = SubmitField('Save')

    def from_model(self, table):
        self.id_.data = table.id

    def to_model(self, table):
        table.id = self.id_.data