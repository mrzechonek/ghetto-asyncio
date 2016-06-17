#!/usr/bin/env python3.5

def periodic_task():
    while True:
        print("> ", end="")
        yield input

task = periodic_task()

for event in task:
    print("[Waiting for %s]" % event, end="")
    event()
    pass
