# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request
from .forms import DynTableForm, DynAttributeForm
from app.extensions import db
from app.models import DynTable, DynAttribute
from app.utils import formToDict, chboxtopy

creator = Blueprint('creator', __name__, template_folder='templates',
                  url_prefix='/creator')


@creator.route('/add', methods=['GET', 'POST'])
def add():
    form = DynTableForm()
    detail_form = DynAttributeForm()
    rform = request.form
    if form.validate_on_submit():
        dynT = DynTable(rform.get('id_'))
        db.session.add(dynT)
        if len(rform) > 2:
            #add detail
            for i in range(1, len(rform) - 1):
                attrDic = formToDict(rform.get('attr_' + str(i)))
                attr = DynAttribute(
                    attrDic.get('attr_name').replace('+',' '), dynT.id,
                    attrDic.get('display').replace('+',' '),
                    attrDic.get('attr_type'), chboxtopy(attrDic.get('pk')),
                    chboxtopy(attrDic.get('required')))
                db.session.add(attr)
        db.session.commit()
        return '1'
    return render_template('index.html', title='DynTable - Add Table',
                           form=form, detail_form=detail_form, url='add')


@creator.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    dT = DynTable.query.get_or_404(id)
    form = DynTableForm()
    detail_form = DynAttributeForm()
    if form.validate_on_submit():
        form.to_model(dT)
        db.session.add(dT)
        db.session.commit()
        return redirect(url_for('creator.list_tables'))
    form.from_model(dT)
    return render_template('index.html', title='DynTable - Edit Table ' + id,
                           form=form, detail_form=detail_form)


@creator.route('/')
def list_tables():
    dT = DynTable.query.all()
    return render_template('list.html', title='DynTable - List of Tables',
                            tables=dT)
