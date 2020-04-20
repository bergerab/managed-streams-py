class Event:
    def __init__(self, value, from_stream, delta_time, time=None):
        self.value = value
        self.from_stream = from_stream
        self.delta_time = delta_time
        self.time = time if time else datetime.utcnow()

        # values taken from the from_stream:
        self.interval = from_stream.interval;
