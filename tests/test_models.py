# -*- coding: utf-8 -*-
from base import BaseTestCase
from app.extensions import db
from app.models import DynTable, DynAttribute


class ModelsTestCase(BaseTestCase):

    def test_dyntables_are_created(self):
        t1 = DynTable('table1')
        t2 = DynTable('table2')
        t3 = DynTable('table3')
        db.session.add_all([t1, t2, t3])
        db.session.commit()
        self.assertEqual(3, len(DynTable.query.all()))

    def test_dyntables_are_deleted(self):
        t1 = DynTable('table1')
        t2 = DynTable('table2')
        t3 = DynTable('table3')
        db.session.add_all([t1, t2, t3])
        db.session.commit()
        ta = DynTable.query.filter_by(id='table1').first()
        db.session.delete(ta)
        db.session.commit()
        self.assertEqual(2, len(DynTable.query.all()))
        ta = DynTable.query.filter_by(id='table1').first()
        self.assertIsNone(ta)

    def test_dyntable_id_are_lowercased(self):
        t1 = DynTable('TABLE1')
        self.assertEqual('table1', t1.id)

    def test_dyntable_id_not_contain_spaces(self):
        t1 = DynTable('table 1')
        self.assertEqual('table_1', t1.id)

    def test_dynattr_are_created(self):
        t1 = DynTable('table1')
        db.session.add(t1)
        db.session.commit()
        a1 = DynAttribute('id', t1.id, 'I', 'Id')
        a2 = DynAttribute('name', t1.id, 'S', 'Name')
        a3 = DynAttribute('description', t1.id, 'S', 'Description')
        db.session.add_all([a1, a2, a3])
        db.session.commit()
        self.assertEqual(3, len(DynAttribute.query.all()))

    def test_dynattr_are_deleted(self):
        t1 = DynTable('table1')
        db.session.add(t1)
        db.session.commit()
        a1 = DynAttribute('id', t1.id, 'I', 'Id')
        a2 = DynAttribute('name', t1.id, 'S', 'Name')
        a3 = DynAttribute('description', t1.id, 'S', 'Description')
        db.session.add_all([a1, a2, a3])
        db.session.commit()
        a = DynAttribute.query.filter_by(id='table1:id').first()
        db.session.delete(a)
        self.assertEqual(2, len(DynAttribute.query.all()))

    def test_dynattr_id_not_contain_spaces(self):
        t1 = DynTable('table1')
        db.session.add(t1)
        db.session.commit()
        a1 = DynAttribute('one item', t1.id, 'I', 'Id')
        self.assertEqual('table1:one_item', a1.id)

    def test_attr_are_deleted_when_dyntable_are_deleted(self):
        t1 = DynTable('table1')
        t2 = DynTable('table2')
        db.session.add_all([t1, t2])
        db.session.commit()
        a1 = DynAttribute('id', t1.id, 'I', 'Id')
        a2 = DynAttribute('name', t1.id, 'S', 'Name')
        a3 = DynAttribute('description', t1.id, 'S', 'Description')
        a4 = DynAttribute('id', t2.id, 'I', 'Id')
        a5 = DynAttribute('name', t2.id, 'S', 'Name')
        a6 = DynAttribute('description', t2.id, 'S', 'Description')
        db.session.add_all([a1, a2, a3, a4, a5, a6])
        db.session.commit()
        db.session.delete(t1)
        db.session.commit()
        attr = DynAttribute.query.filter_by(dyntable_id='table1').first()
        self.assertIsNone(attr)
        attr = DynAttribute.query.filter_by(dyntable_id='table2').first()
        self.assertIsNotNone(attr)
        self.assertEqual(3, len(DynAttribute.query.all()))
