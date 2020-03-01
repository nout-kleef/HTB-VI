
from messageService import MessageService
from secrets import PHONE_NUMBER

class MarketState():
    def __init__(self, stock, feedcode):
        self.messageService = MessageService(PHONE_NUMBER)
        self.stock = stock        
        self.feedcode = feedcode
        self.buy_prices  = list()
        self.sell_prices = list()
        self.entries   = 0
        self.buy_price = None
        self.positions = 0

    def addEntry(self, buy_price, sell_price):
        if self.entries > 52:
            self.buy_prices.pop(0)
            self.sell_prices.pop(0)
        self.buy_prices.append(buy_price)
        self.sell_prices.append(sell_price)
        self.entries = self.entries + 1
        print(self.buy_prices)
        print('entries', self.entries)

    def isEligibleForTradeBuy(self, buy_price):
        if self.entries < 52:
            return False
        conversionLine = self.__calcConversionLine(self.buy_prices)
        baseLine = self.__calcBaseLine(self.buy_prices)
        cloudPoint = self.__getCloud(conversionLine, baseLine, self.buy_prices)
        print(self.stock)        
        print('Conversion line: ', conversionLine, ' > ', baseLine)
        print('Positions:', self.positions)
        print('Cloud Point: ', cloudPoint)
        print('Buy Price ', buy_price)
        print('----------------------')
        if self.__isAboveCloud(cloudPoint, buy_price) and self.positions == 0 and conversionLine > baseLine:
            self.positions = self.positions + 1
            self.buy_price = buy_price
            return True
        return False

    def isEligibleForTradeSell(self, sell_price):
        if self.entries < 52:
            return False
        conversionLine = self.__calcConversionLine(self.sell_prices)
        baseLine = self.__calcBaseLine(self.sell_prices)
        cloudPoint = self.__getCloud(conversionLine, baseLine, self.sell_prices)
        if conversionLine < baseLine and self.buy_price and self.buy_price < sell_price:        
            self.positions = 0
            return True
        return False
        
    def __calcConversionLine(self, prices):
        target_list = prices[-1:-10:-1]    
        highest = max(target_list)
        lowest = min(target_list)
        return (highest+lowest)/2   

    def __calcBaseLine(self, prices):
        target_list = prices[-1:-27:-1]    
        highest = max(target_list)
        lowest = min(target_list)
        return (highest+lowest)/2

    def __calcLeadingSpanA(self, conversionLinePrice, baseLinePrice):
        return (conversionLinePrice + baseLinePrice) / 2      

    def __calcLeadingSpanB(self, prices):
        target_list = prices[-1:-52:-1]    
        highest = max(target_list)
        lowest = min(target_list)
        return (highest+lowest)/2     

    def __getCloud(self, conversionLinePrice, baseLinePrice, prices):
        leadingSpanA = self.__calcLeadingSpanA(conversionLinePrice, baseLinePrice)
        leadingSpanB = self.__calcLeadingSpanB(prices)
        return max(leadingSpanA, leadingSpanB)
    
    def __isAboveCloud(self, cloudPrice, currentAskPrice):
        return currentAskPrice > cloudPrice