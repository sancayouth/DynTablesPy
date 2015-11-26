# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase
from app import create_app
from config import TestConfig


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        pass

    def tearDown(self):
        #db.session.remove()
        #db.drop_all()
        pass