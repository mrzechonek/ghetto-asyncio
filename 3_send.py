#!/usr/bin/env python3.5

def periodic_task():
    while True:
        print("> ", end="")
        text = yield input
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
