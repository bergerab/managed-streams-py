import asyncio
from datetime import datetime

from buffered_channel import BufferedChannel
from event import Event

class Stream:
    def __init__(self, update, interval=0, name=None):
        self.update = update
        self.sources = []
        self.sink = None
        self.data_chan = BufferedChannel()
        
        self.interval = interval # the interval to check the dataChan

        self.cancelled = False

        self.name = name

    def to(self, sink):
        '''
        Connect a sink to this stream
        '''
        self.sink = sink
        self.sink.sources.append(self)

    async def run(self):
        '''
        Start polling for new data on the data channel (for all streams in the network)
        '''
        streams = self.to_list()
        await asyncio.wait([stream.poll_data() for stream in streams])

    async def propagate(self):
        if not self.sources: # if it is a producer
            if not self.sink:
                await self.process(None)                
            else:
                coroutine = self.process(None)
                await self.output(coroutine)
        elif self.sources and self.sink: # if it is a consumer and producer
            event = await self.data_chan.get()
            await self.output(self.process(event))
        else: # if it is a consumer
            event = await self.data_chan.get()
            await self.process(event)
            
    async def process(self, value):
        '''
        Wrapper for the self.update function that adds metric information as an object
        '''

        return await self.update(value)

    async def output(self, coroutine):
        '''
        Wraps a self.process call to take metrics of its running time
        '''

        start_time = datetime.utcnow()

        value = await coroutine
        now = datetime.utcnow()
        
        event = Event(value, self, now - start_time, now)
        self.sink.data_chan.put(event)

    async def poll_data(self):
        while not self.cancelled:
            await self.propagate()
            await asyncio.sleep(self.interval/1000)

    def to_list(self, skip=None):
        '''
        Run a function on each stream in the network
        '''
        if not skip:
            skip = set()

        if self in skip:
            return []

        skip.add(self)

        streams = []
        for source in self.sources:
            streams = source.to_list(skip) + streams

        streams.append(self)
        
        if self.sink:
            streams += self.sink.to_list(skip)

        return streams
