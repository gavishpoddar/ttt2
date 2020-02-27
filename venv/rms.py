from zerodha import *
from data_1m import quoteMoneyControl, getQuote, Quote

def stoploss_at_order(tradingsymbol,transaction_type,order_type,quantity,price):

    if transaction_type == "BUY" :
        price = 0.998 * float(price)
        transaction_type = "SELL"

    if transaction_type == "SELL":
        price = 1.002 * float(price)
        transaction_type = "BUY"

    status_code= 0
    try:
        status_code, order, error_code = create_order(tradingsymbol, transaction_type, "SL-M", quantity, 0 , price)
    except:
        error_code = 1
        order = 0

    return status_code, order, error_code

def stop_loss_plus(portfol, order):
    modify = 0
    ordertype = "SL-M"

    stoploss_price = quoteMoneyControl(portfol["tradingsymbol"])

    getQuote(portfol["tradingsymbol"])
    open_p, high_p, low_p ,close_p = Quote(portfol["tradingsymbol"])

    quantity = int(portfol["quantity"])
    if quantity > 0:
        transaction_type = "SELL"
        stoploss_price = float(stoploss_price)

        if high_p < stoploss_price and  high_p > stoploss_price * 0.998:
            stoploss_price = high_p
        elif high_p * 0.998 < stoploss_price and  high_p * 0.998 > stoploss_price * 0.998:
            stoploss_price = high_p * 0.998
        elif close_p < stoploss_price and  close_p > stoploss_price * 0.998:
            stoploss_price = close_p
        elif close_p * 0.998 < stoploss_price and  close_p * 0.998 > stoploss_price * 0.998:
            stoploss_price = close_p * 0.998
        else :
            stoploss_price = stoploss_price * 0.998


    if quantity < 0:
        transaction_type = "BUY"
        quantity = quantity * -1
        stoploss_price = float(stoploss_price)

        if low_p > stoploss_price and  low_p < stoploss_price * 1.002:
            stoploss_price = low_p
        elif low_p * 1.002 > stoploss_price and  low_p * 1.002 < stoploss_price * 1.002:
            stoploss_price = low_p * 1.002
        elif close_p > stoploss_price and  close_p < stoploss_price * 1.002:
            stoploss_price = close_p

        elif close_p * 1.002 > stoploss_price and  close_p * 1.002 < stoploss_price * 1.002:
            stoploss_price = close_p * 1.002
        else :
            stoploss_price = stoploss_price * 1.002

    for x in order:
        if x["tradingsymbol"] == portfol['tradingsymbol'] and x["order_type"] == "SL-M" and x['status'] == 'TRIGGER PENDING':
            modify = 1
            orderid = str(x['order_id'])
            if stoploss_price > x['trigger_price'] and x["transaction_type"] == 'BUY' :
               stoploss_price =  x['trigger_price']

            if stoploss_price < x['trigger_price'] and x["transaction_type"] == 'SELL' :
               stoploss_price =  x['trigger_price']

    if modify == 1:
        status_code, order, error_code = modity_order(orderid,portfol["tradingsymbol"], transaction_type, ordertype, str(quantity), 0,stoploss_price)
    else:
        status_code, order, error_code = create_order(portfol["tradingsymbol"], transaction_type, ordertype, quantity, 0,stoploss_price)

    return status_code, order, error_code


def delete_order(symbol, order):
    for x in order:
        if symbol == x['tradingsymbol'] and x['status'] == 'TRIGGER PENDING':
            print('deleting order')
            variety = 'regular'
            cancel_order(variety,x['order_id'])


def rms():
    # Update Stop Loss Evey Minute
    status_code, order, error_code = orders()

    status, portfol, error_code= positions()
    for x in portfol:
        if x["quantity"] == 0:
            delete_order(x["tradingsymbol"], order)

        if x["quantity"] != 0 :
            stop_loss_plus(x,order)

    print('RMS Updated')