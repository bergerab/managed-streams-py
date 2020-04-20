class SampleRate:
    MS_IN_A_SEC = 1000;
    
    def __init__(self, rate, infinite=False):
        self.rate = 0 if infinite else rate
        self.infinite = infinite

    def to_interval(sample_rate):
        return 0 if sample_rate.infinite else MS_IN_A_SEC / sample_rate.rate
    
    @staticmethod
    def from_interval(interval):
        return SampleRate(infinite=True) if interval == 0 else MS_IN_A_SEC / interval

