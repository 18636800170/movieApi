from flask import json as _json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 封装操作
class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    # 删除之后需要进行commit（）操作
    def delete(self):
        db.session.delete()

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __json__(self):
        keys = vars(self).keys()
        data = {}
        for key in keys:
            if not key.startswith("_"):
                data[key] = getattr(self, key)
        return data


class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, db.Model):
            return o.__json__()
        return _json.JSONEncoder.default(self, o)
