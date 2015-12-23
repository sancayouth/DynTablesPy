import flask_wtf
from wtforms import StringField, IntegerField, SubmitField, BooleanField

def create_form(table):
    class DynamicForm(flask_wtf.Form):
        pass

    for attr in table.attributes:
        setattr(DynamicForm, attr.display, get_field(attr))
    setattr(DynamicForm, 'Submit', SubmitField('Submit'))
    return DynamicForm()

def get_field(field):
    if field.attr_type == 'I':
        return IntegerField(field.display)
    elif field.attr_type == 'S':
        return StringField(field.display)
    elif field.attr_type == 'B':
        return BooleanField(field.display)
