import logging
from logging import FileHandler, Formatter

import os
from logging.handlers import SMTPHandler

from flask import Flask
from flask_classy import FlaskView

from tigereye.models import db, JSONEncoder


def create_app(config=None):
    # 生成app
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object("tigereye.configs.default.DefaultConfig")
    app.config.from_object(config)
    # 使用配置的json处理方式
    app.json_encoder = JSONEncoder
    # 注册views
    configure_views(app)
    # app的debug模式关闭
    if not app.debug:

        # 邮件配置
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            # app.config['EMAIL_PORT'],
            app.config['ADMINS'],
            'TIGEREYE ALERT',
            credentials=(
                app.config['EMAIL_HOST_USER'],
                app.config['EMAIL_HOST_PASSWORD']
            )
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
                Message Type: %(levelname)s
                Location:     %(pathname)s: %(lineno)d
                Module:       %(module)s
                Function:     %(funcName)s
                Time:         %(asctime)s

                Message:


                %(message)s
                '''))

        app.logger.addHandler(mail_handler)

        # 设置app的logger级别
        app.logger.setLevel(logging.INFO)
        # 指定logger文件名
        file_handle=FileHandler(os.path.join(app.config["LOG_DIR"],"app.log"))
        # 设置logger级别
        file_handle.setLevel(logging.INFO)
        # 设置logger格式
        file_handle.setFormatter(Formatter(
            "%(asctime)s %(levelname)s:%(message)s"
        ))
        # app中logger设置添加配置
        app.logger.addHandler(file_handle)

    # 配置数据库
    db.init_app(app)

    app.logger.info("create app succeful")

    return app


def configure_views(app):
    from tigereye.api.cinema import CinemaView
    from tigereye.api.movie import MovieView
    from tigereye.api.hall import HallView
    from tigereye.api.misc import MiscView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView
    from tigereye.api.order import OrderView

    for view in locals().values():
        # print(view)
        # print(type(view),view)
        # type是所有对象的超类
        if type(view) == type and issubclass(view, FlaskView):
            view.register(app)
