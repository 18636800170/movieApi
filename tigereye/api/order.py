from datetime import datetime

from flask import request
from flask_classy import route

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int
from tigereye.helper.code import Code
from tigereye.models.movie import Movie
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat


class OrderView(ApiView):
    # 退票
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    @route("/refund/", methods=["POST", ])
    def refund(self):
        orderno = request.params["orderno"]
        ticket_flag = request.params["ticket_flag"]
        seats = request.params["sid"]

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {"orderno": orderno}
        # 判断是否出票
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        # 订单是否支付
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        # 判断取票码
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {"ticket_flag": ticket_flag}

        refund_num = PlaySeat.refund(orderno, order.pid, seats)

        if not refund_num:
            return Code.ticket_refund_failed, {}

        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()

        return {
            "refund_num": refund_num
        }

    # 出票
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    @route("/print/", methods=["POST", ])
    def print_ticket(self):
        orderno = request.params["orderno"]
        ticket_flag = request.params["ticket_flag"]
        seats = request.params["sid"]

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {"orderno": orderno}
        # 判断是否出票
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        # 订单是否支付
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        # 判断取票码
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {"ticket_flag": ticket_flag}

        printed_num = PlaySeat.print_ticket(order.sell_order_no, order.pid, seats)

        if not printed_num:
            return Code.ticket_print_failed, {}

        order.status = OrderStatus.printed.value
        order.print_time = datetime.now()
        order.save()
        return {
            "printed_num": printed_num,
        }

    # 获取订单信息
    @route("/ticket_info/")
    @Validator(orderno=str)
    def ticket_info(self):
        orderno = request.params["orderno"]
        order = Order.getby_orderno(orderno)

        if not order:
            return Code.order_does_not_exist, {"orderno": orderno}

        order.play = Play.get(order.pid)
        order.movie = Movie.get(order.play.mid)
        order.ticket = PlaySeat.getby_orderno(orderno)

        return order
