# Novixel's Bot File Setup
# Version 0.1
# BotCfg.py
# May 14, 2021
import os
from pathlib import Path
from configparser import ConfigParser
from datetime import datetime

# Time To Build A Home For The Bots Data!
def BuildBotNest(Portfolio_Name):
    '''BuildBotNest(Portfolio_Name)'''
    # First Figure Out Where We Are?
    fullPath = os.path.realpath(__file__) 
    # Next Find What Street We Are On?
    thisDir = os.path.dirname(fullPath)
    # Now Lets Make A Home For All Our Stuff.
    botFold = thisDir + '\_' + str(Portfolio_Name) 
    # Finnaly Build A Road To Our Home.
    Path(botFold).mkdir(parents=True, exist_ok=True) 
    # *Home Sweet Home*
    os.chdir(botFold) 
    # And Send The Map To Our House If Someone Calls!
    return botFold

# Build Bot Data Files
def BuildBotSettings(path):
    '''BuildBotSettings(path)'''
    config_object = ConfigParser()
    config_object["API"] = {            
        "key"           :   "CoinbaseProAPI key",
        "b64secret"     :   "CoinbaseProAPI b64secret",
        "passphrase"    :   "CoinbaseProAPI passphrase",
        "quote"         :   "Selected Quote Currency"
    }
    config_object["TICKER"] = {
            "trade_id"  :   "Trade ID Number",
            "price"     :   "Current Price",
            "size"      :   "0.000000000000000",
            "time"      :   "2021-05-01T12:00:00.578544Z",
            "bid"       :   "0.000000000000000",
            "ask"       :   "0.000000000000000",
            "volume"    :   "0.000000000000000"
    }
    #Write to a file!!
    with open(path,'w') as conf:
        config_object.write(conf)

def BuildAccSettings(path):
    '''BuildAccSettings(path)'''
    config_object = ConfigParser()
    config_object["OVERVEIW"] = {            
        "total_quote"    :   0,
        "total_sats"     :   0,
        "total_accounts" :   0,
        "last_update"    :   0,
    }
    #Write to a file!!
    with open(path,'w') as conf:
        config_object.write(conf)

def BuildTraSettings(path):
    '''BuildTraSettings(path)'''
    config_object = ConfigParser()
    config_object["TRADE"] = {            
        "LAST_TRADE"      :   0,
    }
    #Write to a file!!
    with open(path,'w') as conf:
        config_object.write(conf)

# (Edit That Config File)
def SaveNewApi(path,key,b64secret,passphrase,quote):
    '''SaveNewApi(path,key,b64secret,passphrase,quote)'''
    c = ConfigParser()
    c.read(path)
    # Get the api from config file
    API = c["API"]
    API["key"] = str(key)
    API["b64secret"] = str(b64secret)
    API["passphrase"] = str(passphrase)
    API["quote"] = str(quote)
    # Write changes back to file
    with open(path, 'w') as conf:
        c.write(conf)

def SaveTicker(path,x , d ):
    c = ConfigParser()
    c.read(path)
    #Get the api from config
    TICKER = c["TICKER"]
    TICKER[str(x)] = d
    with open(path, 'w') as conf:
        c.write(conf)

# Specific Config Read Function
def ReadConfig(path,x):
    """ ConfigPath, "Item"  """
    c = ConfigParser()
    c.read(path)
    #Get Info from config
    API = c["API"]
    return API[x]

def ReadTICKER(path,x):
    """ ConfigPath, 'price', """
    c = ConfigParser()
    c.read(path)
    #Get Info from config
    TICKER = c["TICKER"]
    return TICKER[x]

# ACCOUNTS
def SaveAccount(path,cur, x, d):
    """ AccountPath, Currency, "Key", "Item" """
    c = ConfigParser()
    c.read(path)
    if c.has_section(str(cur + "_ACCOUNT")):
        pass
    else:
        c.add_section(str(cur + "_ACCOUNT"))
    account = c[str(cur + "_ACCOUNT")]
    account[str(x)] = d
    with open(path, 'w') as conf:
        c.write(conf)

def ReadAccount(path,cur,x):
    """ AccountPath, "Currency", "Key" """
    c = ConfigParser()
    c.read(path)
    ACCOUNT = c[str(cur + "_ACCOUNT")]
    return ACCOUNT[x]


def SaveOverveiw(path,x,d):
    """ AccountPath, "Key", "Item" """
    c = ConfigParser()
    c.read(path)
    #Get the api from config
    if c.has_section(str("OVERVEIW")):
        pass
    else:
        c.add_section(str("OVERVEIW"))
    #then edit it
    display = c[str("OVERVEIW")]
    display[str(x)] = d
    with open(path, 'w') as conf:
        c.write(conf)
    return d

def ReadOverveiw(path,x):
    """ AccountPath, "Key" """
    c = ConfigParser()
    c.read(path)
    #Get Info from config
    Overveiw = c["OVERVEIW"]
    return Overveiw[x]

def SaveLastTrade(path,x,d):
    """ AccountPath, "Key", "Item" """
    c = ConfigParser()
    c.read(path)
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if c.has_section((time + ":Filled")):
        pass
    else:
        c.add_section((time + ":Filled"))
    display = c[(time + ":Filled")]
    display[str(x)] = str(d)
    with open(path, 'w') as conf:
        c.write(conf)

def SaveNewTrade(path,x,d):
    """ AccountPath, "Key", "Item" """
    c = ConfigParser()
    c.read(path)
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if c.has_section((time + ":Trade")):
        pass
    else:
        c.add_section((time + ":Trade"))
    display = c[(time + ":Trade")]
    display[str(x)] = str(d)
    with open(path, 'w') as conf:
        c.write(conf)

def LogThis(path,message):
    message = str(message)
    now = datetime.now()
    time = now.strftime("%m/%d/%Y, %H:%M:%S")
    with open(path, 'a') as log:
        Text = (time + ":Log: " + message)
        log.writelines(Text + "\n")
        log.close