from unittest import TestCase
from urllib.parse import urlencode

from flask import json

import tigereye
from tigereye.configs.test import TestConfig
from tigereye.helper.code import Code
from tigereye.models import db
from tigereye.models.cinema import Cinema
from tigereye.models.movie import Movie


class FlaskTestCase(TestCase):
    # 相当于__init__函数
    def setUp(self):
        app = tigereye.create_app(TestConfig)
        # 将所有的logger关掉
        app.logger.disabled = True
        # 创建模拟客户端
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            Cinema.create_test_data(cinema_num=1, hall_num=3, play_num=3)
            Movie.create_test_data()

    def assert_get(self, uri, assertcode=200, method="GET", **params):
        if method == "POST":
            rv = self.app.post(uri, data=params)
        else:
            if params:
                rv = self.app.get("%s?%s" % (uri, urlencode(params)))
            else:
                rv = self.app.get(uri)
        self.assertEqual(rv.status_code, assertcode)
        return rv

    def get200(self, uri, method="GET", **params):
        return self.assert_get(uri, 200, method, **params)

    def get_json(self, uri, method="GET", **params):
        rv = self.get200(uri, method, **params)
        return json.loads(rv.data)

    def get_succ_json(self, uri, method="GET", **params):
        data = self.get_json(uri, method, **params)
        self.assertEqual(data["rc"], Code.succ.value)
        return data
