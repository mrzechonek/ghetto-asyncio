#!/usr/bin/env python3.4
# encoding: utf-8

import os
import sys
import glob
import asyncio
from PyQt5.QtCore import QCoreApplication
from quamash import QEventLoop

try:
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
except ImportError:
    pass

class Mod:
    def __init__(self, path):
        pass

@asyncio.coroutine
def load_mod(path):
    @asyncio.coroutine
    def read(file):
        return file.read()

    sys.stdout.write("Loading mod from {} ".format(path))
    sys.stdout.flush()
    for i in range(0, 3):
        sys.stdout.write(".")
        sys.stdout.flush()
    with open(path) as f:
        content = yield from read(f)
        sys.stdout.write(" ok\n")
        return content

@asyncio.coroutine
def load_all_mods(pattern):
    mods = []
    print("Loading mods from {}".format(pattern))
    for i in glob.iglob(pattern):
        mod = yield from load_mod(i)
        mods.append(mod)
    return mods

@asyncio.coroutine
def do_the_shit():
    mods = yield from load_all_mods("./mods/*.json")
    print(mods)

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    asyncio.async(do_the_shit())
    sys.exit(loop.run_forever())
