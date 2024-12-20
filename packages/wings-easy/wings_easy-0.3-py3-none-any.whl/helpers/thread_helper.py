import concurrent.futures
import threading

from helpers.color_helper import str_yellow
from helpers.time_helper import show_time

executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)


def submit(fun, arg):
    executor.submit(fun, arg)


def run(fun, arg):
    thread_name = threading.current_thread().ident
    print(str_yellow(f"{show_time()}。{'==' * 13} {thread_name} {'==' * 50}"))
    fun(arg)
    print(str_yellow(f"{show_time()}。{'==' * 13} {thread_name} {'==' * 50}"))


def t_log(msg):
    print(f"{show_time()} {threading.current_thread().ident} {msg}")
