#!/usr/bin/env python3.5

from itertools import count

def echo():
    for i in count(1):
        print("%i> " % i, end="")
        text = yield input
        print("Received '%s'" % text)

task = echo()

try:
    event = next(task)
    while event:
        print("[Waiting for %s]" % event, end="")
        result = event()
        event = task.send(result)
except StopIteration:
    pass
