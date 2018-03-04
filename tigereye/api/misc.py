from flask import current_app, request
from flask_classy import FlaskView


# 视图函数
class MiscView(FlaskView):
    # 设置当前视图类的访问路径
    route_base = "/"

    def index(self):
        return self.check()

    def check(self):
        current_app.logger.info("check form %s"%request.remote_addr)
        return "hello"

    def error(self):
        0/1
