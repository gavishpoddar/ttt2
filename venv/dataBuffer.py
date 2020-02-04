import requests
import time
from datetime import date
import os.path

today = date.today()
today = today.strftime("%d%B%Y")


def quote(symbol):
 datafilename = "data/datadump/" + symbol + today + ".txt"

 url = "https://priceapi-aws.moneycontrol.com/pricefeed/nse/equitycash/" + symbol
 payload = {}
 headers = {}
 response = requests.request("GET", url, headers=headers, data = payload)
 data = response.json()
 data = data['data']['pricecurrent']
 with open(datafilename , "a") as myfile:
  myfile.write(data+"\n")
