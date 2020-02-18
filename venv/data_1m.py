import requests
import time
import json
from datetime import datetime
import stocklist

from proxy import proxyList

"""
# Use too conert time zone    =       print(timezn(key))

 from datetime import datetime
 from dateutil import tz

 now = datetime.now()
 now = now.strftime("%Y%m%d %H:%M:%S")


def timezn(now):

 from_zone = tz.gettz('America/New_York')
 to_zone = tz.gettz('Asia/Kolkata')

 utc = datetime.strptime(now, '%Y-%m-%d %H:%M')
 utc = utc.replace(tzinfo=from_zone)
 central = utc.astimezone(to_zone)
 return central
"""


def quoteMoneyControl(symbol):
    for x in stocklist.data:
        if x["symbol"] == symbol:
            symbol = x["mc-symbol"]
        if x["tradingsymbol"] == symbol:
            symbol = x["mc-symbol"]

    url = "https://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/" + symbol
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    data = data['data']['pricecurrent']
    return data


def STOCH(symbol):
    indicator = "STOCH"
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
    try:
      with open(filename) as json_file:
          data = json.load(json_file)
    except:
        getSTOCH(symbol)
        with open(filename) as json_file:
            data = json.load(json_file)

    SlowK = []
    SlowD = []
    hist = []

    data = (data['Technical Analysis: STOCH'])
    keys = data.keys()
    for key in keys:
        SlowK.append(data[key]['SlowK'])
        SlowD.append(data[key]['SlowD'])
        hist.append(float(data[key]['SlowK']) - float(data[key]['SlowD']))
    myDict = {"SlowK": SlowK, "SlowD": SlowD, "Hist": hist}
    return myDict


def RSI(symbol):
    rsi = []
    indicator = "RSI"
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
    try:
      with open(filename) as json_file:
          data = json.load(json_file)
    except:
        getRSI(symbol)
        with open(filename) as json_file:
            data = json.load(json_file)

    data = (data['Technical Analysis: RSI'])
    keys = data.keys()
    for key in keys:
        rsi.append(data[key]['RSI'])
    return rsi

def Quote(symbol):
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/quotes/1min/" + symbol + now + ".txt"

    open_p = []
    high_p = []
    low_p = []
    close_p = [



    ]


    try:
      with open(filename) as json_file:
          data = json.load(json_file)
    except:
        getMACD(symbol)
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/quotes/1min/" + symbol + now + ".txt"
        with open(filename) as json_file:
            data = json.load(json_file)
    data = (data['Time Series (1min)'])
    keys = data.keys()
    for key in keys:
        open_p.append(data[key]['1. open'])
        high_p.append(data[key]['2. high'])
        low_p.append(data[key]['3. low'])
        close_p.append(data[key]['3. close'])

    myDict = {"open": open_p, "high": high_p, "low": low_p, "close": close_p}
    return myDict


def MACD(symbol):
    indicator = "MACD"
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"

    MACD_Signal = []
    MACD = []
    MACD_Hist = []
    try:
      with open(filename) as json_file:
          data = json.load(json_file)
    except:
        getMACD(symbol)
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
        with open(filename) as json_file:
            data = json.load(json_file)
    data = (data['Technical Analysis: MACD'])
    keys = data.keys()
    for key in keys:
        MACD.append(data[key]['MACD'])
        MACD_Signal.append(data[key]['MACD_Signal'])
        MACD_Hist.append(float(data[key]['MACD_Hist']))

    myDict = {"MACD": MACD, "MACD_Signal": MACD_Signal, "Hist": MACD_Hist}
    return myDict


def getMACD(symbol):
    try:
        indicator = "MACD"
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
        url = "https://www.alphavantage.co/query?function=MACD&interval=1min&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=3)
        with open(filename, 'w') as outfile:
            data = response.json()
            test = data['Technical Analysis: MACD']
            json.dump(data, outfile)
    except:
        getMACD(symbol)


def getSTOCH(symbol):
    try:
        indicator = "STOCH"
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
        url = "https://www.alphavantage.co/query?function=STOCH&interval=1min&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=3)
        with open(filename, 'w') as outfile:
            data = response.json()
            test = (data['Technical Analysis: STOCH'])
            json.dump(data, outfile)
    except:
        getSTOCH(symbol)


def getRSI(symbol):
    try:
        indicator = "RSI"
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/indicator/1min/" + indicator + symbol + now + ".txt"
        url = "https://www.alphavantage.co/query?function=RSI&interval=1min&time_period=14&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=3)
        with open(filename, 'w') as outfile:
            data = response.json()
            test = data['Technical Analysis: RSI']
            json.dump(data, outfile)
    except:
        getRSI(symbol)

def getQuote(symbol):
    try:
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/quote/1min/" + symbol + now + ".txt"
        url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=1min&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=3)
        with open(filename, 'w') as outfile:
            data = response.json()
            test = data['Time Series (1min)']
            json.dump(data, outfile)
    except:
        getQuote(symbol)