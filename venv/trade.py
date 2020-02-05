import data_1m
import data_5m
import data_30m
import stocklist
import macd_logic
import rsi_logic
import stoch_logic
from zerodha import create_order, positions
import rules
from datetime import datetime

def order(tradingsymbol,transaction_type,order_type,quantity):
    create_order(tradingsymbol, transaction_type, order_type, quantity)

def trade_1min():
    for x in stocklist.data:
        alloted_quantity = x['quantity']
        macd = data_1m.MACD(x['symbol'])
#        stoch = data_1m.STOCH(x['symbol'])
#        rsi = data_1m.RSI(x['symbol'])

        macd_possible_trade, macd_data = macd_logic.macd(macd)
#        stoch_possible_trade , stoch_data = stoch_logic.stoch(stoch)
#        rsi_possible_trade , rsi_data = rsi_logic.rsi(rsi)

        possible_trade = macd_possible_trade

        quantity = alloted_quantity

        if possible_trade != 0:
            status, portfolio, error_code = positions()
            for portfol in portfolio:
               if portfol['tradingsymbol'] == x['tradingsymbol'] and portfol["quantity"] != 0  :
                  if macd_data['transaction_type'] == "BUY" and portfol["quantity"] < 0 or macd_data['transaction_type'] == "SELL" and portfol["quantity"] > 0:
                     current_quantity = portfol["quantity"]
                     if current_quantity < 0:
                             current_quantity = current_quantity * -1
                     quantity = alloted_quantity + current_quantity


        if macd_possible_trade == 1:
            rules_broken = rules.rules(macd, macd_data['transaction_type'], x['symbol'])
            if rules_broken == 0:
                print("trading")
                order(x['tradingsymbol'], macd_data['transaction_type'], 'MARKET', int(quantity))

def trade_5min():
    if datetime.utcnow().minute % 5 == 0 :
      for x in stocklist.data:
         alloted_quantity = x['quantity']
         macd = data_5m.MACD(x['symbol'])
#         stoch = data_5m.STOCH(x['symbol'])
#         rsi = data_5m.RSI(x['symbol'])

         macd_possible_trade, macd_data = macd_logic.macd(macd)
#         stoch_possible_trade , stoch_data = stoch_logic.stoch(stoch)
#         rsi_possible_trade , rsi_data = rsi_logic.rsi(rsi)

         possible_trade = macd_possible_trade

         quantity = alloted_quantity

         if possible_trade != 0:
             status, portfolio, error_code = positions()
             for portfol in portfolio:
                if portfol['tradingsymbol'] == x['tradingsymbol'] and portfol["quantity"] != 0  :
                   if macd_data['transaction_type'] == "BUY" and portfol["quantity"] < 0 or macd_data['transaction_type'] == "SELL" and portfol["quantity"] > 0:
                      current_quantity = portfol["quantity"]
                      if current_quantity < 0:
                               current_quantity = current_quantity * -1
                      quantity = alloted_quantity + current_quantity

         if macd_possible_trade == 1:
             rules_broken = rules.rules(macd, macd_data['transaction_type'], x['symbol'])
             if rules_broken == 0:
                 print("trading")
                 order(x['tradingsymbol'], macd_data['transaction_type'], 'MARKET', int(quantity))

def trade_30min():
    if datetime.utcnow().minute % 30 == 0 :
      for x in stocklist.data:
         alloted_quantity = x['quantity']
         macd = data_30m.MACD(x['symbol'])
#         stoch = data_5m.STOCH(x['symbol'])
#         rsi = data_5m.RSI(x['symbol'])

         macd_possible_trade, macd_data = macd_logic.macd(macd)
#         stoch_possible_trade , stoch_data = stoch_logic.stoch(stoch)
#         rsi_possible_trade , rsi_data = rsi_logic.rsi(rsi)

         possible_trade = macd_possible_trade

         quantity = alloted_quantity

         if possible_trade != 0:
             status, portfolio, error_code = positions()
             for portfol in portfolio:
                if portfol['tradingsymbol'] == x['tradingsymbol'] and portfol["quantity"] != 0  :
                   if macd_data['transaction_type'] == "BUY" and portfol["quantity"] < 0 or macd_data['transaction_type'] == "SELL" and portfol["quantity"] > 0:
                      current_quantity = portfol["quantity"]
                      if current_quantity < 0:
                               current_quantity = current_quantity * -1
                      quantity = alloted_quantity + current_quantity

         if macd_possible_trade == 1:
             rules_broken = rules.rules(macd, macd_data['transaction_type'], x['symbol'])
             if rules_broken == 0:
                 print("trading")
                 order(x['tradingsymbol'], macd_data['transaction_type'], 'MARKET', int(quantity))