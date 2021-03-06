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
    filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"
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
    filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"
    with open(filename) as json_file:
        data = json.load(json_file)

    data = (data['Technical Analysis: RSI'])
    keys = data.keys()
    for key in keys:
        rsi.append(data[key]['RSI'])
    return rsi


def MACD(symbol):
    indicator = "MACD"
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"

    MACD_Signal = []
    MACD = []
    MACD_Hist = []
    with open(filename) as json_file:
        data = json.load(json_file)
    data = (data['Technical Analysis: MACD'])
    keys = data.keys()
    for key in keys:
        MACD.append(data[key]['MACD'])
        MACD_Signal.append(data[key]['MACD_Signal'])
        MACD_Hist.append(round(float(data[key]['MACD_Hist']), 3))

    myDict = {"MACD": MACD, "MACD_Signal": MACD_Signal, "Hist": MACD_Hist}
    return myDict


def getMACD(symbol):
    try:
        indicator = "MACD"
        now = datetime.now()
        now = now.strftime("%d%m%Y%H:%M")
        filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"
        url = "https://www.alphavantage.co/query?function=MACD&interval=5min&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=5)
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
        filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"
        url = "https://www.alphavantage.co/query?function=STOCH&interval=5min&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=5)
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
        filename = "data/datadump/indicator/5min/" + indicator + symbol + now + ".json"
        url = "https://www.alphavantage.co/query?function=RSI&interval=5min&time_period=14&series_type=close&apikey=6OKA3205BSYK5H0G&symbol=" + symbol
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxyList(), timeout=5)
        with open(filename, 'w') as outfile:
            data = response.json()
            test = data['Technical Analysis: RSI']
            json.dump(data, outfile)
    except:
        getRSI(symbol)
