#!/usr/bin/env python3.5

def async_input():
    text = yield input
    return text

def periodic_task():
    while True:
        print("> ", end="")
        text = yield from async_input()
        print("Received '%s'" % text)

task = periodic_task()

try:
    event = next(task)
    while event:
        print("[Waiting for %s]" % event, end="")
        result = event()
        event = task.send(result)
except StopIteration:
    pass
