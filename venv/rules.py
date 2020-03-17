import logic_calculation
import stocklist

def stock_ckeck(symbol):
  for x in stocklist.data:
      if x['symbol'] == symbol:
          limit = x["lim"]
          no_action_change = float(x["no_action_change"])
          return limit, no_action_change


def macd(macd, symbol):
    limit, no_action_change = stock_ckeck(symbol)
    rules_broken = 0
    if -limit <= macd["Hist"][0] <= limit:
        rules_broken = rules_broken + 1
        print("LIMIT")
    elif -limit <= macd["Hist"][1] <= limit:
        rules_broken = rules_broken + 1
    elif -float(no_action_change) <= macd["Hist"][0] - macd["Hist"][1] <= float(no_action_change):
        print("NO ACTION CHANGE")
        rules_broken = rules_broken + 1

    return rules_broken


def rules(macdindicator ,trade_type, symbol):
     rules_broken = macd(macdindicator, symbol)
     if rules_broken > 0:
         print(symbol)
         print("Brocking Trading BY RULES")
     return rules_broken
