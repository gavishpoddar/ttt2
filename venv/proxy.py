import os
import random
import json
from time import sleep
import datetime



def updateProxy():
   os.system("proxybroker find --types HTTPS -l 30 -f json > /Users/gdev/PycharmProjects/kite_api_2020.02.04/venv/proxylistupdate.json")
   os.rename(
       '/Users/gdev/PycharmProjects/kite_api_2020.02.04/venv/proxylistupdate.json',
       '/Users/gdev/PycharmProjects/kite_api_2020.02.04/venv/proxylist.json')

def proxyList():
    try:
     with open('proxylist.json') as json_file:
         data = json.load(json_file)

     rand = random.randint(0,29)


     host = data[rand]['host']
     port = str(data[rand]['port'])
     https_proxy = "https://"+host+":"+port
    

     proxy = {
         "https": https_proxy
     }
    except:

        updateProxy()
        proxy = proxyList()

    return proxy