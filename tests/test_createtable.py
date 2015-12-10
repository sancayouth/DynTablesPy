# -*- coding: utf-8 -*-
from base import BaseTestCase
from app.models import create_table
from app.extensions import db

class UtilsTestCase(BaseTestCase):

    def test_table_is_created(self):
        table_attr = []
        table_attr.append({'attr_name':'name', 'attr_type':'S'})
        table_attr.append({'attr_name':'id','attr_type':'I', 'pk':True})
        Table = create_table('tablepoc', table_attr)
        db.create_all()
        poc = Table(id=1, name='hello')
        db.session.add(poc)
        db.session.commit()
        self.assertEqual(1, len(Table.query.all()))
        table = Table.query.first()
        self.assertEqual('hello', table.name)        
        self.assertIsNotNone(db.metadata.tables.get('tablepoc'))
