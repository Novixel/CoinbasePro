# Novixel's Bot Authenticated Connection
# Version 0.1
# BotAuth.py
# May 14, 2021
import BotCfg as cfg
from time import sleep
from datetime import datetime
import cbpro
import os

# Coinbase Connection For Our Config Data
class ConnectPort():
    """ Bot Connection To Coinbase"""
    # This will do everything involving the coinbase api!
    auth = None
    quote = None

    def __init__(self,portfolio): # Set up on creation
        print("Initializing",portfolio)
        # Build directory for our config file if not already done
        self.initTime = datetime.now()
        self.path = cfg.BuildBotNest(portfolio)
        self.ConfigPath = (self.path + '\Config.ini')
        self.AccountPath = (self.path + '\Accounts.ini')
        self.TradePath = (self.path + '\Trades.ini')
        self.SATS = 0

        # Lets Build The Config File If We Haven't Already
        if os.path.isfile(self.ConfigPath):
            print("Config File Found\n",(self.ConfigPath))
        else: 
            print("\nConfig File Not Found!\nBuilding Config File!\n")
            cfg.BuildBotSettings(self.ConfigPath)
            print("\nThe Config File Was Created!\n")

        # Then Lets Build The Accounts File If We Haven't Already
        if os.path.isfile(self.AccountPath):
            print("Accounts File Found\n",(self.AccountPath))
            pass 
        else: 
            print("\nAccounts File Not Found!\nBuilding Accounts File!\n")
            cfg.BuildAccSettings(self.AccountPath)
            print("\nThe Accounts File Was Created!\n")

        # Finaly Lets Build The Trade File If We Haven't Already
        if os.path.isfile(self.TradePath):
            print("Trade File Found\n",(self.TradePath))
            pass 
        else: 
            print("\nTrade File Not Found!\nBuilding Trade File!\n")
            cfg.BuildTraSettings(self.TradePath)
            print("\nThe Trade File Was Created!\n")

        # Read & Set API Auth For Coinbase
        if cfg.ReadConfig(self.ConfigPath,"key") == "CoinbaseProAPI key": 
            print("No API Keys Have Been Set!\nPlease Enter Your Coinbase Pro Portfolio API Info!\n")
            key = input("Enter API KEY:\n")
            secret = input("Enter API SECRET:\n")
            passphrase = input("Enter API PASSPHRASE:\n")
            quote = input("Enter Your Main Quote Currency\n")
            cfg.SaveNewApi(self.ConfigPath,key,secret,passphrase,quote)
        else: # Read your already set key
            key = cfg.ReadConfig(self.ConfigPath,"key")
            secret = cfg.ReadConfig(self.ConfigPath,"b64secret")
            passphrase = cfg.ReadConfig(self.ConfigPath,"passphrase")
            quote = cfg.ReadConfig(self.ConfigPath,"quote")

        # Create a authenticated client for the coinbase api
        self.auth = cbpro.AuthenticatedClient(key,secret,passphrase)

        # Add useful data
        self.port = portfolio
        self.quote = quote
        self.name = str(portfolio) + str(quote)
        lastupdate = float(cfg.ReadOverveiw(self.AccountPath, "last_update"))
        hour = self.initTime.hour
        if lastupdate != hour:
            self.CheckAllAccounts()

    def GetLastTrade(self,product_id):
        """Return: Side,Price,Size"""
        filled = self.auth.get_fills(product_id)
        for i in filled:
            # for k,v in i.items():
            #     #print(k,v)
            #     cfg.SaveLastTrade(self.TradePath, k, v)
            side = i["side"]
            price = i['price']
            size = i['size']
            break
        self.lastSide = str(side)
        self.lastPrice = float(price)
        self.lastSize = float(size)
        self.lastProduct = product_id
        return float(price)

    def SendTrade(self,product_id,side,price,size):
        '''SendMarketTrade(pair,side,price,size)'''
        trade = self.auth.place_order(
            product_id= product_id,
            side= side, 
            order_type= 'limit',
            price= price , 
            size= size)
        print("\nTrade Request Sent!")
        for k,v in trade.items():
            print(k,"=\t",v)
            cfg.SaveNewTrade(self.TradePath, k, v)
        print("\n")

    def UpdateAccount(self,Account_id):
        account = self.auth.get_account(Account_id)
        if 'available' in account:
            AvailableBalance = account['available']
        else:
            AvailableBalance = 0
        # Add more here
        return float(AvailableBalance)  

    def GetTicker(self,product_id):
        tick = self.auth.get_product_ticker(product_id)
        for k , v in tick.items():
            cfg.SaveTicker(self.ConfigPath,str(k),str(v))
        return float(tick["price"])

    def CheckAllAccounts(self):
        # Hey Coinbase! May I have my accounts please.
        a = self.auth.get_accounts()
        MainQuote = self.quote # usd, usdc ,eur .. etc

        self.AllAccounts = []
        self.AllBalances = []
        self.AllAvailable = []
        self.BTCValues = []

        print("\n\tSorting All Accounts!\n\nPlease Wait..\n")
        # Lets Check Every Single Account We Have!
        accountCount = 0
        for i in a: 
            # Count Accounts And Grab Data
            accountCount += 1
            cur = str(i["currency"]) # Grab the Accounts Currency Name "BTC"
            avai = float(i["available"]) # Grab The Accounts Available Balance

            # Add Data To List
            self.AllAccounts.append(cur.upper())
            self.AllBalances.append(avai)

            # Save Everything From The Account To Account File
            for k,v in i.items():
                cfg.SaveAccount(self.AccountPath,str(cur),str(k),str(v))
                
            # Now Sort And Get The Prices For All The Accounts
            Quotes = ["USD","USDC","USDT","EUR","GBP"]
            NoBTC = ["BTC","CVC","DAI","DNT","GNT","LOOM","OXT"]
            BrokenQuotes = ["XRP","OXT"]
            if avai > 0 and cur not in BrokenQuotes:
                self.AllAvailable.append(cur.upper())
                if cur in Quotes:
                    product_id = ( "BTC" + "-" + cur )
                    p = self.GetTicker(product_id)
                    price = 1 / p
                    btcValue = avai * price        
                elif cur in NoBTC:
                    if cur == "BTC":
                        price = 1
                        btcValue = avai
                    else:
                        product_id = ( cur + "-" + MainQuote )
                        p = self.GetTicker(product_id)
                        price = 1 / p
                        btcValue = 0
                else:
                    product_id = ( cur + "-" + "BTC" )
                    price = self.GetTicker(product_id)
                    btcValue = avai * price
                self.SATS += btcValue
                cfg.SaveAccount(self.AccountPath,str(cur),"BTC_VALUE",str("%.8f"%btcValue))
            sleep(0.2)

        # End of Account Check loop
        print("\nPORTFOLIO OVERVEIW:\n")
        print("Total Accounts:\t",accountCount)
        time = datetime.now()
        hour = time.hour
        count = 0
        for aa in self.AllAccounts:
            av = self.AllBalances[count]
            if av > 0:
                print(aa , "%.8f"%(self.AllBalances[count]))
            count += 1
        print("\n")
        p = self.GetTicker( ("BTC" + "-" + MainQuote) )
        self.TOTAL_QUOTE = (self.SATS * p)
        cfg.SaveOverveiw(self.AccountPath, "total_quote", "%.2f"%(self.TOTAL_QUOTE))
        cfg.SaveOverveiw(self.AccountPath, "total_sats", "%.8f"%(self.SATS))
        cfg.SaveOverveiw(self.AccountPath, "total_accounts", str(accountCount))
        cfg.SaveOverveiw(self.AccountPath, "last_update", str(hour))
        print("Sats:\t",("%.8f"%(self.SATS)),"BTC")
        print("Quote:\t",("%.2f"%(self.TOTAL_QUOTE)),MainQuote)
        print("Finished @",time)