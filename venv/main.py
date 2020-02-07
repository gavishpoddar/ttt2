import datetime
import time
import threading

import stocklist
from rms import rms
from updates import updates
from trade import trade_1min,trade_5min

start = datetime.time(9, 15, 0)
end = datetime.time(15, 10, 0)

def time_in_range(x):
  if start <= end:
    return start <= x <= end
  else:
    return start <= x or x <= end

def pre_processor():
  data = stocklist.data
  threads = []
  update = threading.Thread(target=rms, args=())
  threads.append(update)

  if time_in_range(datetime.datetime.now().time()) == False:
    print("Not in Trading hours")
    quit()

  for x in data:
     update = threading.Thread(target=updates, args=(x["symbol"], x["mc-symbol"],))
     threads.append(update)

  sleeptime = datetime.datetime.utcnow().second
  if sleeptime > 30:
    sleeptime = 60 - sleeptime
    print("Error Correction Sleep : "+ str(sleeptime))
    time.sleep(sleeptime)

  if sleeptime < 20:
   sleeptime = 20 - datetime.datetime.utcnow().second
   print("Pre- Process Sleep : "+ str(sleeptime))
   time.sleep(sleeptime)

  for x in threads:
     x.start()

  for x in threads:
     x.join()


def post_processor():
  sleeptime = 60 - datetime.datetime.utcnow().second
  if sleeptime > 40:
    sleeptime = 0
  print("Post- Process Sleep : "+ str(sleeptime))
  time.sleep(sleeptime)

while True:
  pre_processor()
  trade_5min()
  post_processor()