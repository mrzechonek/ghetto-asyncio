#!/usr/bin/env python3.5

from itertools import count

def echo():
    for i in count(1):
        print("%i> " % i, end="")
        yield input

task = echo()

try:
    event = next(task)
    while event:
        print("[Waiting for %s]" % event, end="")
        event()
        event = next(task)
except StopIteration:
    pass
