from flask import request

from tigereye.api import ApiView
from tigereye.extensions.validator import Validator
from tigereye.helper.code import Code
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.models.movie import Movie
from tigereye.models.play import Play


class CinemaView(ApiView):
    def all(self):
        cinemas = Cinema.query.all()
        # print(cinemas)
        return cinemas

    # flask定义的可以进行省略
    @Validator(cid=int)
    def get(self):
        cid = request.args["cid"]
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
        return cinema

    # 获取对应的影厅
    @Validator(cid=int)
    def halls(self):
        cid = request.params["cid"]
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, request.args
            # return {"msg": "cinema %s is not found" % cid}
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

    @Validator(cid=int)
    def plays(self):
        cid = request.params["cid"]
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist.request.args
        cinema.plays = Play.query.filter_by(cid=cid).all()
        for play in cinema.plays:
            play.movie = Movie.get(play.mid)
        return cinema
