#!/usr/bin/env python3.5
from itertools import count

def echo():
    for i in count():
        print("%i> " % i, end="")
        yield input

task = echo()

for event in task:
    print("[Waiting for %s]" % event, end="")
    event()
