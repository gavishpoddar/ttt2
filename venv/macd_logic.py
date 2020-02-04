def change(val1, val2):
    return float(val1)-float(val2)

def trend(val1, val2):
    val = change(val1,val2)
    trend1 = 0
    if val > 0:
        trend1 = 1
    if val < 0:
        trend1 = -1
    if val == 0:
        trend1 = 0
    return trend1



def trend_change(val1, val2, val3, val4, val5):

    trend1 = trend(val1,val2)
    trend2 = trend(val2,val3)
    trend3 = trend(val3,val4)
    trend4 = trend(val4,val5)

    trend_change = 0

    if trend1 != trend2 and trend2 == trend3 or trend3 == 0:
        trend_change = 1
    if trend1 != trend3 and trend3 == trend4 or trend4 == 0:
        trend_change = 1
    return trend_change


def trend_change_hist(val1, val2, val3):
    possible_trade = 0

    data = {}

    if val1 > val2 and val3 > val2:
        print(val1)
        print(val2)
        print(val3)

        possible_trade = 1
        data = {"transaction_type" : "BUY"}
    if val1 < val2 and val3 < val2:

        print(val1)
        print(val2)
        print(val3)

        possible_trade = 1
        data = {"transaction_type" : "SELL"}

    return possible_trade, data

def macd(macd):

    possible_trade, data = trend_change_hist(macd['Hist'][0],macd['Hist'][1],macd['Hist'][2])

    """
    trend_c = trend_change(macd["MACD"][0],macd["MACD"][1],macd["MACD"][2],macd["MACD"][3],macd["MACD"][4])
    trend1 = trend(macd["MACD"][0],macd["MACD"][1])

    possible_trade = 0
    data = {}

    if trend_c == 1 and trend1 != 0:
        possible_trade = 1
        if trend1 == 1:
            data = {"transaction_type" : "SELL"}
        if trend1 == -1:
            data = {"transaction_type": "BUY"}
    """

    return possible_trade, data