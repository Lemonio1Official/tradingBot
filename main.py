from config import Config
from Client.Client import Client
from Client.Types import OrderParams
from Client.Calc import avgPrice, Buying, getInitialPurchaseAmount, getInitialPriceChange
from Client.Indicators import Indicators
from Client.Telegram import Telegram
from env import API_KEY, API_SECRET
from typing import List, Any
from time import sleep

client = Client(API_KEY, API_SECRET)

def CancelOrders(orders: List[Any]): pass
def TakeProfitAll(orders: List[Any], price: float): pass
def NotFilled(order): pass
def showOrdersGrid(): pass

def main():
    client.Check()
    if 'code' in client.Leverage(Config.TRADING_PAIR, Config.LEVERAGE):
        raise ValueError('Set leverage error')
    MarginTypeRes = client.MarginType(Config.TRADING_PAIR, 'CROSSED')
    if 'code' in MarginTypeRes:
        if MarginTypeRes['code'] != -4046:
            raise ValueError('Set margin type error')
    if float(client.Balance()['balance']) < Config.DEPOSIT:
        raise ValueError('Insufficient balance')

    symbolInfo = Client.GetSymbolInfo(Config.TRADING_PAIR)

    currentOrder = 0
    overlap = 0
    price_change = 0
    TP_orders = []
    purchases = []
    nextPrice = None
    nextAmount = getInitialPurchaseAmount(Config.DEPOSIT * Config.LEVERAGE, Config.ORDERS_GRID, Config.MARTINGALE)

    while True:
        TP_orders = list(filter(NotFilled, TP_orders))

        if len(purchases) and not len(TP_orders):
            amount = Client.GetTotalAmount(purchases, True)
            Telegram.ProfitMessage(currentOrder, amount)

            currentOrder = 0
            overlap = 0
            price_change = 0
            purchases = []
            nextPrice = None

        if currentOrder == Config.ORDERS_GRID:
            sleep(3)
            continue

        if len(purchases) and purchases[-1]['status'] == 'NEW':
            order = client.Order(OrderParams(Config.TRADING_PAIR ,orderId=purchases[-1]['orderId']), 'info')
            if order['status'] == 'FILLED':
                    purchases[-1] = order
                    amount = Client.GetTotalAmount(purchases)
                    averagePrice = Client.AvgPrice(purchases)
                    Telegram.DealDetails(currentOrder, amount, averagePrice)

        Checking = 0
        for i in Config.FILTERS:
            if i['filter'] == 'RSI':
                rsi = Indicators.RSI(Config.TRADING_PAIR, i['interval'])
                if rsi == None:
                    continue
                if rsi >= i['value']:
                    Checking = rsi - i['value']
                    break
        if Checking != 0:
            sleep(6) if Checking > 10 else sleep(3)
            continue

        price = client.GetPrice(Config.TRADING_PAIR)

        if nextPrice:
            if Config.SIDE == 'BUY':
                if price > nextPrice:
                    sleep(3)
                    continue
            else:
                if price < nextPrice:
                    sleep(3)
                    continue

        if currentOrder == 0:
            overlap = price * Config.PRICE_OVERLAP
            nextPrice = price
            price_change = overlap / (Config.ORDERS_GRID - 1)
            if Config.LOGARITHMIC:
                price_change = price * getInitialPriceChange(Config.LOGARITHMIC_VALUE, Config.ORDERS_GRID, Config.PRICE_OVERLAP)

            showOrdersGrid(overlap, nextPrice, nextAmount, price_change, symbolInfo)
            Telegram.SendMessage(f"🔔 {Config.TRADING_PAIR}\n\nThe bot entered the trade")

        quantity = round(nextAmount / price, symbolInfo['quantityPrecision'])
        purchases.append(client.Order(OrderParams(Config.TRADING_PAIR, Config.SIDE, 'LIMIT', quantity, round(price, symbolInfo['pricePrecision']))))
        Telegram.SendMessage(f"🎣 {Config.TRADING_PAIR}\n\nOrder {currentOrder+1}/{Config.ORDERS_GRID} was placed")

        averagePrice = Client.AvgPrice(purchases)
        TP_price = averagePrice + averagePrice * Config.PROFIT * (1 if Config.SIDE == 'BUY' else -1)

        if len(TP_orders):
            CancelOrders(TP_orders)
            TP_orders = TakeProfitAll(purchases, round(TP_price, symbolInfo['pricePrecision']))
        else:
            TP_orders = TakeProfitAll(purchases, round(TP_price, symbolInfo['pricePrecision']))

        currentOrder += 1

        if Config.LOGARITHMIC:
            nextPrice += price_change * (-1 if Config.SIDE == 'BUY' else 1)
            price_change *= Config.LOGARITHMIC_VALUE
        else:
            nextPrice += overlap / (Config.ORDERS_GRID - 1) * (-1 if Config.SIDE == 'BUY' else 1)

        nextAmount += nextAmount * Config.MARTINGALE

        sleep(3)

def CancelOrders(orders: List[Any]):
    for i in orders:
        client.Order(OrderParams(Config.TRADING_PAIR, orderId=i['orderId']), 'cancel')
        sleep(0.5)

def TakeProfitAll(orders: List[Any], price: float):
    side = 'SELL' if Config.SIDE == 'BUY' else 'BUY'
    TP_orders = []
    for i in orders:
        order = client.Order(OrderParams(Config.TRADING_PAIR, side, 'TAKE_PROFIT', i['origQty'], price, price, orderId=i['orderId']))
        TP_orders.append(order)
        sleep(0.5)

    return TP_orders

def NotFilled(order):
    info = client.Order(OrderParams(Config.TRADING_PAIR, orderId=order['orderId']), 'info')
    sleep(0.5)
    return info['status'] != 'FILLED'

def showOrdersGrid(overlap: float, nextPrice: float, nextAmount: float, price_change: float, symbolInfo: Any):
    orders = []

    while len(orders) < Config.ORDERS_GRID:
        quantity = round(nextAmount / nextPrice, symbolInfo['quantityPrecision'])
        orders.append({"price": round(nextPrice, symbolInfo['pricePrecision']), "origQty": quantity})

        profit = Client.GetTotalAmount(orders, True) * Config.PROFIT
        orders[-1]['profit'] = round(profit, 4)

        if Config.LOGARITHMIC:
            nextPrice += price_change * (-1 if Config.SIDE == 'BUY' else 1)
            price_change *= Config.LOGARITHMIC_VALUE
        else:
            nextPrice += overlap / (Config.ORDERS_GRID - 1) * (-1 if Config.SIDE == 'BUY' else 1)

        nextAmount += nextAmount * Config.MARTINGALE

    orders.append({"totalAmount": Client.GetTotalAmount(orders, True)})

    import json
    print(json.dumps(orders, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
