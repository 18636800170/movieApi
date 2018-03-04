"""
id
影院id
影厅id
电影id
排期id
取票码
票数
金额
支付时间
取票时间
退款时间
创建时间
最后一次更新时间
状态
"""
from enum import unique, Enum
from random import randint

from sqlalchemy import text, func

from tigereye.helper import tetime
from tigereye.models import db, Model


# 对订单表的状态进行定义
@unique
class OrderStatus(Enum):
    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6


class Order(db.Model, Model):
    __tablename__ = "orders"
    # 自己的订单号
    oid = db.Column(db.String(32), primary_key=True)
    # 第三方订单号
    sell_order_no = db.Column(db.String(32), index=True)

    cid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    sid = db.Column(db.String(32))

    # 取票码
    ticket_flag = db.Column(db.String(64))
    # 票数
    ticket_num = db.Column(db.Integer)
    # 金额
    amount = db.Column(db.Integer)
    # 支付时间
    paid_time = db.Column(db.DATETIME)
    # 取票时间
    print_time = db.Column(db.DATETIME)
    # 退款时间
    refund_time = db.Column(db.DATETIME)
    created_time = db.Column(db.DATETIME, server_default=text("CURRENT_TIMESTAMP"))
    updated_time = db.Column(db.DATETIME, onupdate=func.now())

    status = db.Column(db.Integer, default=0, index=True, nullable=False)

    # 定义类方法
    @classmethod
    # 创建订单表
    def create(cls, cid, pid, sid):
        order = cls()
        # 购买时间+随机6位数字+排期id
        order.oid = "%s%s%s" % (tetime.now(), randint(100000, 999999), pid)

        order.pid = pid
        order.cid = cid

        # 对sid进行组合，以便进行保存
        if type(sid) == list:
            order.sid = ",".join(str(i) for i in sid)
        else:
            order.sid = sid

        return order

    @classmethod
    # 通过orderno获取order对象
    def getby_orderno(cls, orderno):
        return Order.query.filter_by(sell_order_no=orderno).first()

    # 生成取票码
    def gen_ticket_flag(self):
        self.ticket_flag = "".join([str(randint(1000, 9999)) for i in range(8)])

    # 判断取票码
    def validate(self, ticket_flag):
        return self.ticket_flag == ticket_flag

    # 通过取票码获取order对象
    @classmethod
    def getby_ticket_flag(cls,ticket_flag):
        return cls.query.filter_by(ticket_flag=ticket_flag).first()
