from datetime import datetime

from flask import request
from flask_classy import route

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, multi_comlex_int
from tigereye.helper.code import Code
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat


class SeatView(ApiView):
    # 进行过滤操作
    @Validator(pid=int, sid=multi_int, price=int, orderno=str)
    # 定义路径和传输协议
    @route('/lock/', methods=["POST", ])
    # 座位锁定操作
    def lock(self):
        # 获取当前所有的需要的属性
        pid = request.params["pid"]
        sid = request.params["sid"]
        price = request.params["price"]
        orderno = request.params["orderno"]
        # 从Play中获取目标对象
        play = Play.get(pid)
        # 判断目标排期是否存在
        if not play:
            return Code.play_does_not_exist, request.params
        # 票价判断：不能低于最低价
        if price < play.lowest_price:
            return Code.prcice_less_than_the_lowest_price, request.params

        # 座位锁定操作
        locked_seat_num = PlaySeat.lock(orderno, pid, sid)
        # 如果没有完成坐定操作，报错
        if not locked_seat_num:
            return Code.seat_lock_failed, {}
        # 表单创建
        order = Order.create(play.cid, pid, sid)
        # 修改第三方的订单号
        order.sell_order_no = orderno
        # 修改订单的状态
        order.status = OrderStatus.locked.value
        # 修改订单锁定的座位数
        order.ticket_num = locked_seat_num
        # 执行保存操作
        order.save()
        # 返回锁定的座位数目
        return {"locked_seats_num": locked_seat_num}

    # 定义路径和传输协议
    @route("/unlock/", methods=["POST", ])
    # 执行过滤操作
    @Validator(pid=int, sid=multi_int, orderno=str)
    # 座位解锁操作
    def unlock(self):
        # 获取对应的值
        pid = request.params["pid"]
        sid = request.params["sid"]
        orderno = request.params["orderno"]
        # 获取目标对象
        play = Play.get(pid)
        # 判断是否存在
        if not play:
            return Code.play_does_not_exist, request.params
        # 获取目标对象
        order = Order.getby_orderno(orderno)
        # 判断是否存在
        if not order:
            return Code.order_does_not_exist, request.params
        # 解锁的座位数目
        unlock_seats_num = PlaySeat.unlock(orderno, pid, sid)
        # 判断解锁操作是否执行
        if not unlock_seats_num:
            return Code.seat_unlock_failed, {}
        # 修改状态
        order.status = OrderStatus.unlocked.value
        # 执行修改保存
        order.save()
        return {"unlock_seats_num": unlock_seats_num}

    @Validator(seats=multi_comlex_int, orderno=str)
    @route("/buy/", methods=["POST", ])
    # 购买
    def buy(self):
        seats = request.params["seats"]
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        # 判断目标order是否存在
        if not order:
            return Code.order_does_not_exist, request.params
        # 判断订单状态是否位锁定
        if order.status != OrderStatus.locked.value:
            # 不是锁定状态报错
            return Code.order_status_error, {
                "orderno": orderno,
                "status": order.status,
            }
        # 修改订单
        order.sell_order_no = request.params["orderno"]
        order.amount = order.amount or 0
        # 座位id
        sid_list = []
        # 计算价钱
        for sid, handle_fee, price in seats:
            sid_list.append(sid)
            order.amount += handle_fee + price
        # 座位购买数量
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        # 判断操作是否成功
        if not bought_seats_num:
            return Code.seat_buy_failed, {}

        order.ticket_num = len(seats)
        order.status = OrderStatus.paid.value
        order.paid_time = datetime.now()
        order.gen_ticket_flag()
        order.save()

        return {
            "bought_seats_num": bought_seats_num,
            "ticket_flag": order.ticket_flag,
        }

