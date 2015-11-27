# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from .forms import DynTableForm
from app.extensions import db
from app.models import DynTable

creator = Blueprint('creator', __name__, template_folder='templates',
                  url_prefix='/creator')


@creator.route('/add', methods=['GET', 'POST'])
def add():
    form = DynTableForm()
    if form.validate_on_submit():
        dynT = DynTable(form.id_.data)
        db.session.add(dynT)
        db.session.commit()
        return redirect(url_for('creator.list_tables'))
    return render_template('index.html', title='DynTable - Add Table',
                           form=form)


@creator.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    dT = DynTable.query.get_or_404(id)
    form = DynTableForm()
    if form.validate_on_submit():
        form.to_model(dT)
        db.session.add(dT)
        db.session.commit()
        return redirect(url_for('creator.list_tables'))
    form.from_model(dT)
    return render_template('index.html', title='DynTable - Edit Table ' + id,
                           form=form)


@creator.route('/')
def list_tables():
    dT = DynTable.query.all()
    return render_template('list.html', title='DynTable - List of Tables',
                            tables=dT)