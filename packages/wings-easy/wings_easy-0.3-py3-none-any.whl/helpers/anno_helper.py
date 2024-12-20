import bisect
import time
from functools import wraps

from helpers.color_helper import str_cyan, str_yellow, str_magenta
from helpers.file_helper import file_parent_directory, file_sub_directory, file_load_py_from_directory
from helpers.re_helper import str_to_pattern
from helpers.static_global import annotated_func
from helpers.thread_helper import submit, t_log


def action_dispatch(text, arg):
    for re_fun in annotated_func:
        if re_fun.pattern.match(text):
            print(str_cyan(f"------- match => {re_fun}"))
            submit(re_fun.fun, arg)
            return re_fun
    return None


class ReFun:
    def __init__(self, key, pattern, desc, priority, fun):
        self.key = key
        self.fun = fun
        self.desc = desc
        self.pattern = pattern
        self.priority = priority

    def __lt__(self, other):
        if not isinstance(other, ReFun):
            return NotImplemented
        return self.priority < other.priority

    def __str__(self):
        return f"【{self.key}】=> {self.desc}"


# 自定义注解
def action(pattern, desc, priority=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t_log(str_yellow(f"{'==' * 13} {func.__name__} {args} {kwargs} {'==' * 50}"))
            start_time = time.time()  # 记录开始时间
            result = func(*args, **kwargs)  # 执行被装饰的函数
            end_time = time.time()  # 记录结束时间
            elapsed_time = end_time - start_time  # 计算耗时
            t_log(str_yellow(f"{'==' * 13} {func.__name__} {args} {kwargs} cost:{elapsed_time:.2f}s {'==' * 50}"))
            return result

        re_fun = ReFun(pattern, str_to_pattern(pattern), desc, priority, wrapper)
        # annotated_functions.append(re_fun)
        # 使用 bisect.insort 插入元素,添加的时候就排序
        bisect.insort(annotated_func, re_fun)
        t_log(str_magenta(f"register action -> {re_fun} =>{len(annotated_func)}->{id(annotated_func)}"))
        return wrapper

    return decorator


def scan_and_import(directory):
    print(f"Scanning directory: {directory}")
    """扫描目录并导入所有Python文件"""
    file_load_py_from_directory(directory)


if __name__ == "__main__":
    # 扫描当前目录下的所有Python文件
    scan_and_import(file_sub_directory(file_parent_directory("."), "test"))
    print(id(annotated_func))
    for func in annotated_func:
        print(f"Found annotated function: {func}")

    action_dispatch("3", "nihao")
