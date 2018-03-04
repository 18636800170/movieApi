from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat, SeatType


class PlayView(ApiView):

    @Validator(pid=int)
    def seats(self):
        pid = request.params["pid"]
        return PlaySeat.query.filter(
            PlaySeat.pid == pid,
            PlaySeat.seat_type != SeatType.road.value,
        ).all()

    def get(self):
        pid=request.params["pid"]
        return Play.get(pid)
