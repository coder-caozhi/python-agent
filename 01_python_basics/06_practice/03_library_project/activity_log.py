"""给借书和还书共用的装饰器，只记录成功的操作。"""

from functools import wraps


def log_action(action: str):
    def decorate(function):
        # 每个被装饰的函数各自保存一份成功次数。
        successful_calls = 0

        @wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal successful_calls  # 修改 decorate 里保存的计数。
            # * 和 ** 展开收到的参数。原函数抛出异常时，下面两行不会执行。
            result = function(*args, **kwargs)
            successful_calls += 1
            print(f"{action}成功（第 {successful_calls} 次）｜{result}")
            return result

        return wrapper

    return decorate
