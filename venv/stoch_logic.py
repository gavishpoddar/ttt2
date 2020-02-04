max_level = 80
high_level = 60
low_level = 40
min_level = 20
base = 50


def change(val1, val2):
   return val1 - val2


def trend(val1, val2):
   val = change(val1, val2)

   if val >= 0:
      trend1 = 1
   if val <= 0:
      trend1 = -1
   return trend1


def trend_change(val1, val2, val3, val4=0):
   trend1 = trend(val1, val2)
   trend2 = trend(val2, val3)
   trend3 = trend(val3, val4)

   trend_change = 0

   if trend1 != trend2:
      trend_change = 1
   if val4 != 0:
      if trend1 != trend3:
         trend_change = 1
   return trend_change


def trend_reversal(val1, val2, val3):
   trendChange = trend_change(val1, val2, val3)

   trendReversal = 0
   if trendChange == 1:
      if val2 >= max_level or val2 <= min_level:
         trendReversal = 1

   return trendReversal


def level(val1, val2):
   if (val1 <= base or val2 <= base):
      lev = -1
      if (val1 <= low_level or val2 <= low_level):
         lev = -2
         if (val1 <= min_level or val2 <= min_level):
            lev = -3

   if (val1 >= base or val2 >= base):
      lev = 1
      if (val1 >= high_level or val2 >= high_level):
         lev = 2
         if (val1 >= max_level or val2 >= max_level):
            lev = 3

   return lev


def cross_over(val1, val2, val3, val4):
   cros_ovr = 0
   cros_ovr_type = 0
   if val1 > 0 and val2 < 0:
      cros_ovr = 1
      cros_ovr_type = -1

   if val1 < 0 and val2 > 0:
      cros_ovr = 1
      cros_ovr_type = 1

   if val1 > 0 and val3 < 0:
      cros_ovr = 1
      cros_ovr_type = -1

   if val1 < 0 and val3 > 0:
      cros_ovr = 1
      cros_ovr_type = 1

   if val1 > 0 and val4 < 0:
      cros_ovr = 1
      cros_ovr_type = -1

   if val1 < 0 and val4 > 0:
      cros_ovr = 1
      cros_ovr_type = 1

   return cros_ovr, cros_ovr_type

def stoch(stoch):
   possible_trade = 0
   data = {}
   return possible_trade, data