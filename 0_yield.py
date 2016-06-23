#!/usr/bin/env python3.5

from itertools import count


def echo():
    for i in count():
        print("%i> " % i, end="")
        yield

task = echo()

for i in task:
    print("[Waiting for input]", end="")
    input()
