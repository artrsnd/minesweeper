# -*- coding: utf-8 -*-

import threading

from functools import wraps


def thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!
    return run
