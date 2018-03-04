from datetime import datetime


# 对时间进行转换
def now():
    # 将时间转换成对定的格式
    return datetime.now().strftime("%Y%m%d%H%M%S")
