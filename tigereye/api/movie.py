from flask import jsonify
from flask_classy import FlaskView

from tigereye.api import ApiView
from tigereye.models.movie import Movie


class MovieView(ApiView):
    def all(self):
        movies = Movie.query.all()
        # print(movies)
        return movies