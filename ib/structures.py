'''
Created on Jul 6, 2015

@author: Adam
'''

class Contract:
    def __init__(self,
                 conId = 0,
                 symbol = '',
                 secType = '',
                 expiry = '',
                 strike = 0.0,
                 right = '',
                 multiplier = '',
                 exchange = '',
                 currency = '',
                 localSymbol = '',
                 tradingClass = '',
                 primaryExch = '',
                 includeExpired = False,
                 secIdType = '',
                 secId = '',
                 comboLegsDescrip = '',
                 comboLegs = None,
                 underComp = None):
        self.conId = conId
        self.symbol = symbol
        self.secType = secType
        self.expiry = expiry
        self.strike = strike
        self.right = right
        self.multiplier = multiplier
        self.exchange = exchange
        self.currency = currency
        self.localSymbol = localSymbol
        self.tradingClass = tradingClass
        self.primaryExch = primaryExch
        self.includeExpired = includeExpired
        self.secIdType = secIdType
        self.secId = secId
        self.comboLegsDescrip = comboLegsDescrip
        self.comboLegs = comboLegs
        self.underComp = underComp
        
    def __call__(self):
        return [self.conId,
                self.symbol,
                self.secType,
                self.expiry,
                self.strike,
                self.right,
                self.multiplier,
                self.exchange,
                self.currency,
                self.localSymbol,
                self.tradingClass,
                self.primaryExch,
                self.includeExpired,
                self.comboLegsDescrip,
                self.comboLegs,
                self.underComp]

class ContractDetails:
    def __init__(self):
        self.summary = None
        self.marketName = ''
        self.minTick = 0.
        self.priceMagnifier = 0
        self.orderTypes = ''
        self.validExchanges = ''
        self.underConId = 0
        self.longName = ''
        self.contractMonth = ''
        self.industry = ''
        self.category = ''
        self.subcategory = ''
        self.timeZoneId = ''
        self.tradingHours = ''
        self.liquidHours = ''
        self.evRule = ''
        self.evMultiplier = 0.
        self.secIdList = None
        self.cusip = ''
        self.ratings = ''
        self.descAppend = ''
        self.bondType = ''
        self.couponType = ''
        self.callable = False
        self.putable = False
        self.coupon = 0.
        self.convertible = False
        self.maturity = ''
        self.issueDate = ''
        self.nextOptionDate = ''
        self.nextOptionType = ''
        self.nextOptionPartial = False
        self.notes = ''
         
    def populate_from_buffer(self, buf):
        data = buf.next()[0]
        replaceEmptyListWithNone(data)
        self.summary = Contract(*data)
        
def replaceEmptyListWithNone(data):
    for i in xrange(len(data)):
        if data[i] == []:
            data[i] = None
            print 'replaced empty list with None'