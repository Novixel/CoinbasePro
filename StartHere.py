# Welcome To Novixel's Crypto Trading Application!
# v0.01
# StartHere.py
# May 14, 2021
import BotAuth
import BotTrade
port = BotAuth.ConnectPort("BOT")
trade = BotTrade.Trade(port)
trade.SetTrade("BTC","USDC")
count = 0
while True:
    trade.TradeLoop()
    count +=1
    print(count)