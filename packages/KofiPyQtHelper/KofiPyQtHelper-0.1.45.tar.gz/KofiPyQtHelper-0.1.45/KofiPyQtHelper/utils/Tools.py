#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2024-03-08 10:54:54
LastEditors  : Kofi
LastEditTime : 2024-03-27 19:42:20
Description  : 工具函数
"""
import time
import cProfile
from loguru import logger
from io import StringIO
from pstats import Stats
from functools import wraps


class Tools:
    def timing_decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} 耗时 {end - start} 秒")
            return result

        return wrapper

    def profile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            result = func(*args, **kwargs)
            profiler.disable()
            # 使用 StringIO 捕获输出
            s = StringIO()
            stats = Stats(profiler, stream=s).sort_stats("cumulative")
            stats.print_stats()
            s.seek(0)  # 移动到字符串的开头
            # 将输出记录到 loguru 日志
            logger.info(s.read().strip())  # 使用 strip() 去除可能的额外空白行
            return result

        return wrapper
