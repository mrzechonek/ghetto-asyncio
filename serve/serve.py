#!/usr/bin/env python3.5

import sys
asyncio = __import__(sys.argv[1])

from echo import server

loop = asyncio.get_event_loop()

loop.create_task(server(loop, ('localhost', 1234)))
loop.run_forever()
