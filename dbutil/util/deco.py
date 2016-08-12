#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger, StreamHandler, Formatter, INFO


logger = getLogger(__file__)
logger.setLevel(INFO)
handler = StreamHandler()
handler.setFormatter(Formatter(fmt='%(asctime)s %(levelname)s %(message)s',
                               datefmt='%Y-%m-%d %I:%M:%S',))
logger.addHandler(handler)


def logging(func):
    "Decorator"
    def wrapper(obj, *args, **kwargs):
        logger.debug(func.__qualname__ + " START")

        result = func(obj, *args, **kwargs)

        logger.debug(func.__qualname__ + " END")
        return result
    return wrapper
