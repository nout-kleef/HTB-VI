import autotrader_template
import Histogram
import MarketState


class Trader():
    INSTRUMENTS = ["SP-FUTURE", "ESX-FUTURE"]

    def __init__(self, conversionLine, baseLine, spanB, source):
        self.marketHistory = []
        for instr in Trader.INSTRUMENTS:
            self.marketHistory.add(Histogram(spanB, instr))
        # start listening
        self.listen(source)

    def listen(self, source):
        pass
