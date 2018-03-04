from tigereye.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    JSON_SORT_KEYS = False
    # 关闭自动格式json
    JSON_PRETTYPRINT_REGULAR = False
    #
    SQLALCHEMY_ECHO = False
    # 发送邮件
    # import sys
    #  print(sys.path)

    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465

    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'test1@iguye.com'
    # EMAIL_HOST_USER = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    EMAIL_USE_SSL = True
    ADMINS = ['870444708@qq.com']