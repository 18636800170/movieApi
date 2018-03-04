from .helper import FlaskTestCase


class TestApiCinema(FlaskTestCase):
    def test_cinema_all(self):
        self.get_succ_json("/cinema/all/")

    def test_cinema_halls(self):
        self.assert_get("/cinema/halls/", 400)
        data = self.get_succ_json("/cinema/halls/", cid=1)
        self.assertIsNotNone(data["data"])
