import functools

from flask import request, jsonify

from tigereye.helper.code import Code


class Validator(object):
    # 初始化函数
    def __init__(self, **parameter_template):
        # 获取对应的参数
        self.pt = parameter_template

    # 当类调用的时候自动调用
    def __call__(self, f):
        # 将原本的方法的参数赋给新的方法
        @functools.wraps(f)
        def decorated_funtion(*args, **kwargs):
            try:
                request.params = {}
                for k, v in self.pt.items():
                    # 对所有的数值执行对应的规范
                    request.params[k] = v(request.values[k])
            except Exception:
                # 对response进行编写
                response = jsonify(
                    rc=Code.required_parameter_missing.value,
                    msg=Code.required_parameter_missing.name,
                    data={"require_param": k}
                )
                # 对responsse进行赋值
                response.status_code = 400
                # 返回response
                return response
            # 执行原本的函数
            return f(*args, **kwargs)

        return decorated_funtion


class ValidatorError(Exception):
    def __init__(self, message, values):
        super(ValidatorError, self).__init__(message)
        self.values = values


# 执行多个转换成整形
def multi_int(values, sperator=","):
    return [int(i) for i in values.split(sperator)]


def comlex_int(values, sperator="-"):
    digits = values.split(sperator)
    result = []
    for digit in digits:
        # 判断字符串是否是纯数字构成
        if not digit.isdigit():
            raise ValidatorError("comlexx int error :%s " % values, values)
        result.append(int(digit))
    return result


def multi_comlex_int(values, sperator=","):
    return [comlex_int(i) for i in values.split(sperator)]
