class Histogram():
    def __init__(self, size, instrument):
        self.size = size
        self.instrument = instrument
        self.histogram = []

    def marketUpdate(self, newState):
        if len(self.histogram) > self.size:
            del self.histogram[0]
        self.histogram.add(newState)
