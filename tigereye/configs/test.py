from tigereye.configs.default import DefaultConfig


class TestConfig(DefaultConfig):
    # 测试开启
    TESTING=True
    # 输出json的时候会根据字母进行排序
    JSON_SORT_KEYS=True
    # 关闭显示sql
    SQLALCHEMY_ECHO=False
    # 存储在sqlite上
    SQLALCHEMY_DATABASE_URI ="sqlite://"
