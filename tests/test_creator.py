# -*- coding: utf-8 -*-
from base import BaseTestCase
from app.extensions import db
from app.models import DynTable


class CreatorTestCase(BaseTestCase):

    def test_add_route_works_as_expected(self):
        response = self.client.get('/creator/add', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_edit_route_works_as_expected(self):
        db.session.add(DynTable('table'))
        db.session.commit()
        response = self.client.get('/creator/edit/table',
                   content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_add_table(self):
        response = self.client.post(
            '/creator/add',
            data=dict(id_='table test'),
            follow_redirects=True
        )
        self.assertIn(b'DynTable - List of Tables', response.data)
        self.assertIn(b'table_test', response.data)
        ta = DynTable.query.filter_by(id='table_test').first()
        self.assertIsNotNone(ta)