# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from app.extensions import db
from app.models import DynTable
from app.dynamic_form import create_form
from app.dynamic_class import loadClass

tables = Blueprint('tables', __name__, template_folder='templates',
                  url_prefix='/tables')


@tables.route('/<table_id>/add', methods=['GET', 'POST'])
def view_table(table_id):
    dT = DynTable.query.get_or_404(table_id)
    form = create_form(dT)
    rform = request.form
    if form.validate_on_submit():
        dyn_class = loadClass(table_id)
        dc = dyn_class()
        for attr in dT.attributes:
            if not attr.pk:
                setattr(dc, attr.attr_name.lower(), \
                    rform.get(attr.display))
        db.session.add(dc)
        db.session.commit()
    return render_template('view.html', title=dT.id, form_title=dT.id.upper() \
    , form=form)

@tables.route('/')
def show_tables():
    dyn_table = DynTable.query.all()
    return render_template('list_tables.html', tables=dyn_table, \
                title='DynTable - List of Tables')
