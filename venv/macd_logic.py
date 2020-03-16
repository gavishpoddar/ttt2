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
    possible_trade = 0
    data = {}

    if trend1 != trend2 and trend2 == trend3 or trend3 == 0:
        trend_change = 1
    if trend1 != trend3 and trend3 == trend4 or trend4 == 0:
        trend_change = 1

    if  trend_change == 1:
        if trend1 ==  1:
            possible_trade = 1
            data = {"transaction_type": "BUY"}

        if trend1 ==  -1:
            possible_trade = 1
            data = {"transaction_type": "SELL"}


    return possible_trade, data


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

    possible_trade, data = trend_change(macd['Hist'][0],macd['Hist'][1],macd['Hist'][2],macd['Hist'][3],macd['Hist'][4])
    print(data)
    return possible_trade, data