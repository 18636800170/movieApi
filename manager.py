from flask_script import Manager, Server, Shell

from tigereye.app import create_app
from tigereye.models import db
from tigereye.models.cinema import Cinema
from tigereye.models.movie import Movie

app = create_app()
manager = Manager(app)


# 对shell方法进行自动化生成属性
def _make_context():
    locals().update(globals())
    return dict(**locals())


# 注册runserver，开启服务器,同时定义host和port
manager.add_command("runserver", Server("127.0.0.1", port=5000))
# 对shell方法进行重写注册
manager.add_command("shell", Shell(make_context=_make_context))


# 删除db
@manager.command
def dropdb():
    db.drop_all()


# 创建db
@manager.command
def createdb():
    db.create_all()


# 创建测试数据
@manager.command
def testdata():
    Movie.create_test_data()
    Cinema.create_test_data()


# 更新db
@manager.command
def initdb():
    dropdb()
    createdb()
    testdata()


if __name__ == '__main__':
    manager.run()
