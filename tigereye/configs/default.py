import os


class DefaultConfig(object):
    # 项目根目录
    BASE_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))

    # debug开启
    DEBUG = True

    # 配置数据库路径
    TYPE = "mysql+pymysql"
    USERNAME = "root"
    PASSSWORD = "root"
    HOST = "127.0.0.1"
    PORT = 3306
    DATABASENAME = "tigereye"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@127.0.0.1/tigereye"
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(TYPE, USERNAME, PASSSWORD, HOST, PORT, DATABASENAME)

    # 关闭数据库提示
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 打印sql语句
    SQLALCHEMY_ECHO=True
    # 设置log日志的路径
    LOG_DIR=os.path.join(BASE_DIR,"logs")

