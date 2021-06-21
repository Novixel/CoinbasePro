# Novixel's Bot Trading Class
# v0.01
# Trading.py
# May 14, 2021
from datetime import datetime
from time import sleep
import BotCfg as cfg 

class Trade():
    Port = object
    Switch = None
    def __init__(self,port):
        '''Requires Connected Portfolio'''
        print("\nTrade Initializing:",port.name)
        self.StartTime = datetime.now()
        self.port = port
        self.MainQuote = port.quote
        self.MainQuoteid = cfg.ReadAccount(self.port.AccountPath,str(self.MainQuote),"id")
        self.MainBal = self.port.UpdateAccount(self.MainQuoteid)
        self.QuoteBal = 0
        self.BaseBal = 0
        self.StartHour = port.initTime.hour
        self.CurrentHour = self.StartHour
        
    def SetTrade(self,BaseCurrency,QuoteCurrency):
        '''SetTrade(self,BaseCurrency,QuoteCurrency)'''
        self.StartTotal = self.port.SATS
        self.BaseCurrency = BaseCurrency
        self.QuoteCurrency = QuoteCurrency
        self.Quoteid = cfg.ReadAccount(self.port.AccountPath,str(self.QuoteCurrency),"id")
        self.Baseid = cfg.ReadAccount(self.port.AccountPath,str(self.BaseCurrency),"id")
        self.Product = str(self.BaseCurrency + "-" + self.QuoteCurrency)
        self.StartQuote = self.port.UpdateAccount(self.Quoteid)
        self.StartBase = self.port.UpdateAccount(self.Baseid)
        self.StartPrice = self.port.GetTicker(self.Product)
        print("Product = ",self.Product)
        print("Starting at = ",self.StartPrice)
        self.Update()

    def Update(self):
        self.CurrentTime = datetime.now()
        self.CurrentHour = self.CurrentTime.hour
        self.CurrentMin = self.CurrentTime.min
        self.MainBal = self.port.UpdateAccount(self.MainQuoteid)
        self.QuoteBal = self.port.UpdateAccount(self.Quoteid)
        self.BaseBal = self.port.UpdateAccount(self.Baseid)
        if self.CurrentHour != self.StartHour:
            self.StartHour = self.CurrentHour
            self.port.CheckAllAccounts()
            

    def TradeLoop(self):
        loops = 300
        loop = 0
        while loop != loops:
            loop += 1
            print("\nMarket Check #",loop, "/", loops)
            self.MainTrade()
            print("\n")
            if self.Switch == "Stable":
                sleep(900)
                self.Switch == None
            elif self.Switch == "Buy":
                sleep(150)
                self.Switch == None
            elif self.Switch == "Sell":
                sleep(150)
                self.Switch == None
            if loop % 30 == 0:
                self.Update()
            sleep(1.33)

    def MainTrade(self):
        CurrentPrice = self.port.GetTicker(self.Product)
        quos = ["BTC","BCH","ETH","LTC"]
        if self.BaseCurrency == quos[0]:
            minTradeQuote = 0.0001
            minTradeBase = 0.0001
        elif self.BaseCurrency != quos[0] and self.BaseCurrency in quos:
            minTradeQuote = 0.001
            minTradeBase = 0.001
        elif self.QuoteCurrency == quos[0] and self.BaseCurrency not in quos:
            minTradeQuote = 1 / CurrentPrice
            minTradeBase = 1
        else:
            print("MINTRADE ERROR")
            exit()
        print("Minimum Trade Size:")
        print("\t%.5f"%minTradeBase,self.BaseCurrency)
        print("\t%.5f"%(minTradeQuote*CurrentPrice),self.QuoteCurrency)
        LastTradePrice = self.port.GetLastTrade(self.Product)
        LastTradeSide = self.port.lastSide
        print("Last Trade Price Was","%.5f"%LastTradePrice,self.BaseCurrency)
        print("Last Trade Side Was A",LastTradeSide)
        CurrQuote = self.port.UpdateAccount(self.Quoteid)
        CurreBase = self.port.UpdateAccount(self.Baseid)
        print(self.BaseCurrency,"has","%.5f"%CurreBase,"available")
        print(self.QuoteCurrency,"has","%.5f"%CurrQuote,"available")
        print("\nChecking",self.Product,"Market")
        count = 0
        while self.Switch == None:
            count +=1 
            CurrentPrice = self.port.GetTicker(self.Product)
            if CurrentPrice > LastTradePrice:
                inc = CurrentPrice - LastTradePrice
                perc = inc / LastTradePrice * 100
                if perc > 0.5 and count % 10 == 0:
                    print("\nCurrent:\t",self.Product,CurrentPrice,self.QuoteCurrency)
                    print("Price is up\t +" + "%.2f"%perc + "% Since last trade")
                elif perc > 0.1 and count % 5 == 0:
                    print("\n")
                    print(self.CurrentTime)
                    print(self.Product,CurrentPrice,self.QuoteCurrency)
                if CurrQuote >= minTradeQuote:
                    if 1 >= perc >= 0.9:
                        print("Sending Min Sell Trade")
                        self.port.SendTrade(self.Product, "sell", CurrentPrice, minTradeBase)
                        self.Switch = "Sell"
                    elif 2 >= perc >= 1:
                        print("Sending Min*1.5 Sell Trade")
                        size = minTradeBase * 1.5
                        self.port.SendTrade(self.Product, "sell", CurrentPrice, minTradeBase)
                        self.Switch = "Sell"
                    elif perc >= 2:
                        print("Sending Min*2 Buy Trade")
                        size = minTradeBase * 2
                        self.port.SendTrade(self.Product, "sell", CurrentPrice, size)
                        self.Switch = "Sell"
            elif CurrentPrice < LastTradePrice:
                dec = LastTradePrice - CurrentPrice
                perc = dec / LastTradePrice * 100
                if perc > 0.5 and count % 5 == 0:
                    print("\nCurrent:\t",self.Product,CurrentPrice,self.QuoteCurrency)
                    print("Price is down\t -" + "%.2f"%perc + "% Since last trade")
                elif perc > 0.1 and count % 5 == 0:
                    print("\n")
                    print(self.CurrentTime)
                    print(self.Product,CurrentPrice,self.QuoteCurrency)
                if CurreBase > minTradeBase:
                    if 1 >= perc >= 0.9:
                        print("Sending Min Buy Trade")
                        self.port.SendTrade(self.Product, "buy", CurrentPrice, minTradeBase)
                        self.Switch = "Buy"
                    elif 2 >= perc >= 1:
                        print("Sending Min*1.5 Buy Trade")
                        size = minTradeBase * 1.5
                        self.port.SendTrade(self.Product, "buy", CurrentPrice, size)
                        self.Switch = "Buy"
                    elif perc >= 2:
                        print("Sending Min*2 Buy Trade")
                        size = minTradeBase * 2
                        self.port.SendTrade(self.Product, "buy", CurrentPrice, size)
                        self.Switch = "Buy"
            sleep(1.33)


