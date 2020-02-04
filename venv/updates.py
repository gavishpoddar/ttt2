from datetime import datetime
import threading
import time
import data_1m
import data_5m
from dataBuffer import quote

def updates(symbol, moneyControl_Symbol):
 threads = []

 min5 = 0
 min1 = 1

 if min1 == 1 :
   macd_1m =  threading.Thread(target=data_1m.getMACD, args=(symbol,))
   ltp_1m =  threading.Thread(target=quote, args=(moneyControl_Symbol,))
   threads.append(macd_1m)
   threads.append(ltp_1m)

 if datetime.utcnow().minute % 5 == 0 and min5 == 1:

   macd_5m = threading.Thread(target=data_5m.getMACD, args=(symbol,))
   ltp_5m = threading.Thread(target=quote, args=(moneyControl_Symbol,))
   threads.append(macd_5m)
   threads.append(ltp_5m)

 for x in threads:
     x.start()

 for x in threads:
     x.join()