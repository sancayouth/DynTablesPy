# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request
from .forms import DynTableForm, DynAttributeForm
from app.extensions import db
from app.models import DynTable, DynAttribute
from app.utils import formToDict, chboxtopy
from app.dynamic_class import create_table


creator = Blueprint('creator', __name__, template_folder='templates',\
                  url_prefix='/creator')


@creator.route('/add', methods=['GET', 'POST'])
def add():
    form = DynTableForm()
    detail_form = DynAttributeForm()
    rform = request.form
    if form.validate_on_submit():
        dyn_table = DynTable(rform.get('id_'))
        db.session.add(dyn_table)
        if len(rform) > 2:
            #add detail
            attr_list = []
            for i in range(1, len(rform) - 1):
                attr_dic = formToDict(rform.get('attr_' + str(i)))
                attr = DynAttribute(
                    attr_dic.get('attr_name').replace('+', ' '), dyn_table.id,
                    attr_dic.get('display', '').replace('+', ' '),
                    attr_dic.get('attr_type')[0], chboxtopy(attr_dic.get('pk')),
                    chboxtopy(attr_dic.get('required')))
                attr_list.append(attr_dic)
                db.session.add(attr)
        db.session.commit()
        create_table(rform.get('id_'), attr_list)
        db.create_all()
        #should create the table on DB
        return '1'
    return render_template('index.html', title='DynTable - Add Table',
                           form=form, detail_form=detail_form, url='add')


@creator.route('/edit/<table_id>', methods=['GET', 'POST'])
def edit(table_id):
    dyn_table = DynTable.query.get_or_404(table_id)
    form = DynTableForm()
    detail_form = DynAttributeForm()
    if form.validate_on_submit():
        form.to_model(dyn_table)
        db.session.add(dyn_table)
        db.session.commit()
        return redirect(url_for('creator.list_tables'))
    form.from_model(dyn_table)
    return render_template('index.html', title='DynTable - Edit Table '\
         + table_id,form=form, detail_form=detail_form)



@creator.route('/')
def list_tables():
    dyn_table = DynTable.query.all()
    return render_template('list.html', title='DynTable - List of Tables', \
                            tables=dyn_table)
