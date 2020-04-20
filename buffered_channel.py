import asyncio

class BufferedChannel:
    def __init__(self):
        self.buffer = []
        self.subscribers = []

    def put(self, value):
        if self.subscribers:
            while self.subscribers:
                self.subscribers.pop().set_result(value)
        else:
            self.buffer.append(value) # everything will be in the wrong order

    def get(self):
        future = asyncio.Future()        
        if self.buffer:
            value = self.buffer.pop()
            future.set_result(value)
        else:
            self.subscribers.append(future)
        return future
    
