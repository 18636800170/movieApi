from flask import request

from tigereye.api import ApiView
from tigereye.helper.code import Code
from tigereye.models.hall import Hall
from tigereye.models.seat import Seat


class HallView(ApiView):
    def seats(self):
        hid = request.args["hid"]
        hall = Hall.get(hid)
        if not hall:
            # return jsonify({"msg":"hall %s is not found"%hid})
            return Code.hall_does_not_exist, request.args
        hall.seats = Seat.query.filter_by(hid=hid).all()
        return hall
