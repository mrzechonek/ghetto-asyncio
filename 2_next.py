#!/usr/bin/env python3.5

def periodic_task():
    while True:
        print("> ", end="")
        yield input

task = periodic_task()

try:
    event = next(task)
    while event:
        print("[Waiting for %s]" % event, end="")
        event()
        event = next(task)
except StopIteration:
    pass
