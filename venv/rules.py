import logic_calculation
import stocklist

def stock_ckeck(symbol):
  for x in stocklist.data:
      if x['symbol'] == symbol:
          min_limit = x["min_lim"]
          max_limit = x["max_lim"]
          return min_limit, max_limit


def macd(macd, symbol):
    min_limit, max_limit = stock_ckeck(symbol)
    rules_broken = 0
    if min_limit <= macd["Hist"][0] <= max_limit:
        rules_broken = rules_broken + 1
    elif min_limit <= macd["Hist"][1] <= max_limit:
        rules_broken = rules_broken + 1

    return rules_broken


def rules(macdindicator ,trade_type, symbol):
     rules_broken = macd(macdindicator, symbol)
     if rules_broken > 0:
         print(symbol)
         print("Brocking Trading BY RULES")
     return rules_broken
