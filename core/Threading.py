# -*- coding: utf-8 -*-

import threading

from functools import wraps


def thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!
    return run


def limit(number):
    """
    Decorator to limit the number of simultaneous threads
    :param number: fumber of simultaneous threads
    :return: function to be executed by a thread
    """
    sem = threading.Semaphore(number)

    def wrapper(func):
        @wraps(func)
        def wrapped(*args):
            with sem:
                return func(*args)
        return wrapped
    return wrapper


def async_t(f):
    """
    This decorator executes a function in a thread
    :param f: function to be executed in a thread
    :return:
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
