import asyncio
from datetime import datetime
import time

from stream import Stream

import random
async def rand(e):
    return random.choice([1,2,3,4,5])

async def show(e):
    print(e.value + 2)
    
s1 = Stream(rand, interval=500, name='a')
s2 = Stream(show, interval=0, name='b')
s1.to(s2)

def run():
    def wakeup():
        '''
        Hack for asyncio on windows where SIGINT wouldn't register
        '''
        loop.call_later(0.5, wakeup)

    
    loop = asyncio.get_event_loop()
    loop.call_later(0.5, wakeup)
    loop.run_until_complete(s1.run())

    
if __name__ == '__main__':
    run()
