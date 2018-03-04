from datetime import datetime
from enum import unique, Enum

from sqlalchemy import text

from tigereye.models import db, Model

"""
id
影厅id
影院id
类型
是否是情侣座
x坐标
y坐标
区域
状态
排
列

"""


@unique
class SeatStatus(Enum):
    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已打票"""
    printed = 3
    """已预订"""
    booked = 9
    """维修中"""
    repair = 99


@unique
class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2
    """保留座位"""
    reserve = 3
    """残疾专座"""
    for_disable = 4
    """VIP专座"""
    vip = 5
    """震动座椅"""
    shake = 6


class Seat(db.Model, Model):
    __tablename__ = "seat"
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    row = db.Column(db.String(16))
    column = db.Column(db.String(16))

    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    lova_seat = db.Column(db.String(16))

    status = db.Column(db.Integer, nullable=False, default=0, index=True)


"""
id
订单号
排期id
座位id
影院id
影厅id
座位类型
是否试情侣座
x坐标
y坐标
排
列
区域
状态
锁定时间
创建时间
"""


class PlaySeat(db.Model, Model):
    __tablename__ = "playseat"
    psid = db.Column(db.Integer, primary_key=True)
    orderno = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)

    pid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    row = db.Column(db.String(16))
    column = db.Column(db.String(16))

    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    lova_seat = db.Column(db.String(16))

    status = db.Column(db.Integer, nullable=False, default=0, index=True)

    lock_time = db.Column(db.DATETIME)
    create_time = db.Column(db.DATETIME, server_default=text("CURRENT_TIMESTAMP"))

    # 执行复制操作
    def copy(self, seat):
        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.seat_type = seat.seat_type
        self.love_seat = seat.lova_seat
        self.status = seat.status

    @classmethod
    # 进行锁定操作
    def lock(cls, orderno, pid, sid_list):
        # 创建session
        session = db.create_scoped_session()
        # 直接对PlaySeat进行操作
        # 进行锁定操作，修改订单号和状态
        rows = session.query(PlaySeat).filter(
            PlaySeat.pid == pid,
            PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.sid.in_(sid_list),
            #     进行修改
        ).update({
            "orderno": orderno,
            "status": SeatStatus.locked.value,
            "lock_time": datetime.now()
            #    关闭同步session操作
        }, synchronize_session=False)
        # 如果操作没有成功，执行rollback回滚
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    # 进行解锁操作
    @classmethod
    def unlock(cls, orderno, pid, sid_list):
        # 创建一个db.session对象
        session = db.create_scoped_session()
        # 完成解锁操作
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value
        ).update({
            "orderno": None,
            "status": SeatStatus.ok.value,
        }, synchronize_session=False)
        # 判断是否进行了解锁
        if rows != len(sid_list):
            session.rollback()
            return 0
        # 进行提交
        session.commit()
        return rows

    # 购买操作
    @classmethod
    def buy(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value,
        ).update({
            "status": SeatStatus.sold.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    # 退票
    @classmethod
    def refund(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value,
        ).update({
            "status": SeatStatus.ok.value,
            "orderno": None,
        }, synchronize_session=False)

        if rows != len(sid_list):
            session.rollback()
            return 0

        session.commit()
        return rows

    # 出票
    @classmethod
    def print_ticket(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value,
        ).update({
            "status": SeatStatus.printed.value,
        }, synchronize_session=False)

        if rows != len(sid_list):
            session.rollback()
            return 0

        session.commit()
        return rows

    # 获取数据
    @classmethod
    def getby_orderno(cls, orderno):
        return cls.query.filter_by(orderno=orderno).all()
