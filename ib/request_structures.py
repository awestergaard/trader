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
