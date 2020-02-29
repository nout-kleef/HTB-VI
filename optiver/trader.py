import autotrader_template
import Histogram
import MarketState


class Trader():
    INSTRUMENTS = ["SP-FUTURE", "ESX-FUTURE"]
    BALANCE = 20_000

    def __init__(self, conversionLine, baseLine, spanB, source):
        self.marketHistory = [] ## list of histograms for both markets
        for instr in Trader.INSTRUMENTS:
            self.marketHistory.add(Histogram(spanB, instr))
        
        self.listen(source)# start listening
        self.conversionLine = conversionLine
        self.baseLine = baseLine
        self.spanB = spanB


    def listen(self, source): ## parses if source == CSV and listens if live
        if source == "CSV":
            with open(r'C:\Users\F.K\Desktop\HTB\HTB-VI\market_data.csv') as market_data:
                for line in market_data:
                    parts = line.split(",")
                    Timestamp = parts[0]   ## as string
                    instrument = parts[1]  ## as string
                    bid_price = float(parts[2])  
                    bid_volume = int(parts[3]) 
                    ask_price = float(parts[4])
                    ask_volume = int(parts[5])
                    market_state = MarketState(bid_price, ask_price, bid_volume, ask_volume) ## update the class if we want more than these
                    self.update_market(market_state, instrument)
                    self.tradeCSV() 

        else:
            start_autotrader() ### not sure about this tbh but this is where we listen from in our design
            ## IMPLEMENT LIVETRADE()

    def update_market(self, market_state, instrument):
        index = self.marketHistory.index(instrument)
        self.marketHistory[index].marketUpdate(market_state)

    def tradeCSV(self):
        pass ## add algorithm here and check the constructor for our data