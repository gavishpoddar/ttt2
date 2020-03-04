import json
import requests
from datetime import date, datetime
import os.path
import time

today = date.today()
today = today.strftime("%d%B%Y")

authfilename = "data/auth/" + today + ".txt"

def myroun(x,transaction_type, prec=2, base=.05):
    # use this in if statement to select the best ratte but the given statemt gives constant//   x = x - 0.05 + x % 0.05
  x =  float(x)
  if x % 0.05 == 0:
      pass
  else:
      if transaction_type == "BUY":
        x = x - 0.05 + x % 0.05
      if transaction_type == "SELL":
        x = x + 0.05 - x % 0.05
  return round(base * round(float(x)/base),prec)

def auth():
   from seleniumwire import webdriver
   from selenium.webdriver.common.keys import Keys
   from selenium.webdriver.common.action_chains import ActionChains

   userName = 'GM5930'
   passWord = 'Archidply1'
   loginpin = '805580'

   browser = webdriver.Chrome("/Users/gavish/PycharmProjects/kite_rest_api/venv/chromedriver",seleniumwire_options={'verify_ssl': False})
   browser.get('https://kite.zerodha.com/')
   username = browser.find_elements_by_css_selector(".uppercase input")
   username[0].send_keys(userName)
   password = browser.find_elements_by_css_selector(".su-input-group+ .su-input-group input")
   password[0].send_keys(passWord)
   loginButton = browser.find_elements_by_css_selector(".wide")
   loginButton[0].click()
   time.sleep(1)
   pin = browser.find_elements_by_css_selector("input")
   pin[0].send_keys(loginpin)
   pinLoginButton = browser.find_elements_by_css_selector(".wide")
   pinLoginButton[0].click()
   time.sleep(10)
   cookies = browser.get_cookies()
   kf_session = cookies[0]['value']
   cfduid = cookies[1]['value']
   for request in browser.requests:
       if request.headers:
           if request.path == "https://kite.zerodha.com/oms/user/profile/full":
               authtoken =  request.headers['Authorization']

   ## Saving DATA
   browser.quit()
   with open(authfilename, 'w') as the_file:
       the_file.write(kf_session +"\n"+ cfduid +"\n"+ authtoken +"\n")
   return kf_session, cfduid, authtoken


if os.path.isfile(authfilename):
    f = open(authfilename,'r').read().splitlines()
    kf_session= f[0]
    cfduid= f[1]
    authtoken= f[2]
else:
    kf_session, cfduid, authtoken = auth()

try:
    url = "https://kite.zerodha.com/oms/user/margins"
    payload = {}

    headers = {
        'authority': 'kite.zerodha.com',
        'x-kite-version': '2.3.0',
        'origin': 'https://kite.zerodha.com',
        'authorization': authtoken,
        'content-type': 'application/x-www-form-urlencoded',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'x-kite-userid': 'GM5930',
        'dnt': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://kite.zerodha.com/dashboard',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        margin = response.json()
    except:
        import brotli
        margin = brotli.decompress(response.content)
        margin = json.loads(margin)
    margin = margin['data']['equity']['available']['live_balance']
    if response.status_code != 200:
        kf_session, cfduid, authtoken = auth()
except:
    kf_session, cfduid, authtoken = auth()


def create_order(tradingsymbol,transaction_type,order_type,quantity,price = 0, stoploss = 0):
  url = "https://kite.zerodha.com/oms/orders/regular"
  stoploss = str(myroun(stoploss,transaction_type))
  quantity= str(quantity)
  price = str(price)
  payload = 'exchange=NSE&tradingsymbol='+tradingsymbol+'&transaction_type='+transaction_type+'&order_type='+order_type+'&quantity='+quantity+'&price='+price+'&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price='+stoploss+'&squareoff=0&stoploss=0&trailing_stoploss=0&variety=regular&user_id=GM5930'

  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }

  status_code = 0

  print("craeting order")

  try:
    response = requests.request("POST", url, headers=headers, data=payload)
    order = response.json()
    order = order['data']['order_id']
    error_code = 0
    status_code = response.status_code
    with open('data/order/placed_order'+ order, 'a') as the_file:
        the_file.write('Order_ID'+ order + 'PAYLOAD'+ payload)
    return status_code, order , error_code
  except:
      error_code = 1
      order = 0
      return status_code, order, error_code


def modity_order(order_id,tradingsymbol,transaction_type,order_type,quantity,price = 0, stoploss = 0):
  stoploss = str(myroun(stoploss,transaction_type))
  price = str(myroun(price,transaction_type))

  print("modify order")

  url = "https://kite.zerodha.com/oms/orders/regular/" + order_id
  payload = 'exchange=NSE&tradingsymbol='+tradingsymbol+'&transaction_type='+transaction_type+'&order_type='+order_type+'&quantity='+quantity+'&price='+price+'&product=MIS&validity=DAY&disclosed_quantity=0&trigger_price='+stoploss+'&squareoff=0&stoploss=0&trailing_stoploss=0&variety=regular&user_id=GM5930'

  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }

  status_code = 0

  try:
    response = requests.request("PUT", url, headers=headers, data=payload)
    order = response.json()
    order = order['data']['order_id']
    error_code = 0
    status_code = response.status_code
    with open('data/order/placed_order'+ order, 'a') as the_file:
        the_file.write('Order_ID'+ order + 'PAYLOAD'+ payload)
    return status_code, order , error_code
  except:
      error_code = 1
      order = 0
      return status_code, order, error_code


def margin():
  url = "https://kite.zerodha.com/oms/user/margins"
  payload = {}

  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }
  status_code = 0

  try:
    response = requests.request("GET", url, headers=headers, data=payload)
    margin = response.json()
    margin = margin['data']['equity']['available']['live_balance']
    error_code = 0
    status_code = response.status_code
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/margin/" + now + ".txt"
    with open(filename, 'w') as outfile:
        json.dump(margin, outfile)
    return status_code, margin, error_code
  except:
      error_code = 1
      return status_code, margin, error_code



def cancel_order(variety,order_number):
  url = "https://kite.zerodha.com/oms/orders/" + variety + "/" + order_number
  payload = {}


  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }
  status_code = 0
  try:
      response = requests.request("DELETE", url, headers=headers, data=payload)
      status_code = 0
      status_code = response.status_code
      return status_code

  except:
      error_code = 1
      return status_code, error_code


def positions():
  url = "https://kite.zerodha.com/oms/portfolio/positions"

  payload = {}

  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }

  status_code = 0

  try:
    order = []
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    for x in range(len(data['data']['day'])):
        myDict = {"tradingsymbol": data['data']['day'][x]['tradingsymbol'], "exchange": data['data']['day'][x]['exchange'],"quantity": data['data']['day'][x]['quantity']}
        order.append(myDict)
    error_code = 0
    status_code = response.status_code
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/position/" + now + ".txt"
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    print(12)

    return status_code, order , error_code
  except:
      error_code = 1
      order = 0
      return status_code, order, error_code


def orders():
  url = "https://kite.zerodha.com/oms/orders"

  payload = {}

  headers = {
    'authority': 'kite.zerodha.com',
    'x-kite-version': '2.3.0',
    'origin': 'https://kite.zerodha.com',
    'authorization': authtoken,
    'content-type': 'application/x-www-form-urlencoded',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'x-kite-userid': 'GM5930',
    'dnt': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'referer': 'https://kite.zerodha.com/dashboard',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '__cfduid=' + cfduid + ';  kf_session=' + kf_session
  }

  status_code = 0

  try:
    order = []
    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()
    for x in range(len(data['data'])):
        myDict = {"order_id": data['data'][x]['order_id'], "status": data['data'][x]['status'],"quantity": data['data'][x]['quantity'],"exchange": data['data'][x]['exchange'], "tradingsymbol": data['data'][x]['tradingsymbol'],"order_type": data['data'][x]['order_type'],"transaction_type": data['data'][x]['transaction_type'],"price": data['data'][x]['price'],"trigger_price": data['data'][x]['trigger_price'],"filled_quantity": data['data'][x]['filled_quantity'],"pending_quantity": data['data'][x]['pending_quantity']}
        order.append(myDict)
    error_code = 0
    status_code = response.status_code
    now = datetime.now()
    now = now.strftime("%d%m%Y%H:%M")
    filename = "data/datadump/orders/" + now + ".txt"
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

    return status_code, order , error_code
  except:
      error_code = 1
      order = 0
      return status_code, order, error_code
