from sqlalchemy import text, func

from tigereye.models import db, Model

"""
id
电影id
影院id
影厅id
价格类型
原价
售价
最低价
开始时间
时长
创建时间
最后更新时间
状态
"""


class Play(db.Model, Model):
    __tablename__ = "play"
    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    mid = db.Column(db.Integer)

    start_time = db.Column(db.DATETIME, nullable=False)
    # 时长
    duration = db.Column(db.Integer, default=0, nullable=False)

    price_type = db.Column(db.Integer)
    price = db.Column(db.Integer)
    market_price = db.Column(db.Integer)
    lowest_price = db.Column(db.Integer)
    # 在服务器段进行时间的定义
    created_time = db.Column(db.DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    # 当修改的时候获取时间
    updated_time = db.Column(db.DATETIME, onupdate=func.now())
    status = db.Column(db.Integer, nullable=False, default=0, index=True)
