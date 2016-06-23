#!/usr/bin/env python3.5

from itertools import count


def async_input():
    text = yield input
    return text


def echo():
    for i in count():
        print("%i> " % i, end="")
        text = yield from async_input()
        print("Received %s" % text)

task = echo()

try:
    event = next(task)
    while event:
        print("[Waiting for %s]" % event, end="")
        result = event()
        event = task.send(result)
except StopIteration:
    pass
