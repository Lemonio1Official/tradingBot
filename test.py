# -- create & cancel order
# order = client.Order(OrderParams('ETHUSDT', 'BUY', 'LIMIT', 0.01, 2250))
# sleep(3)
# print(client.Order(OrderParams('ETHUSDT', orderId=order['orderId']), True))

# -- create order with takeProfit & stopLoss
# order = client.Order(OrderParams('ETHUSDT', 'BUY', 'LIMIT', 0.01, 2250))
# print(client.Order(OrderParams('ETHUSDT', 'SELL', 'TAKE_PROFIT', 0.01, 2350, 2350, orderId=order['orderId'])))
# print(client.Order(OrderParams('ETHUSDT', 'SELL', 'STOP', 0.01, 2200, 2200, orderId=order['orderId'])))

# -- change leverage
# client.Leverage('ETHUSDT', 5)

# -- change margin type
# client.MarginType('ETHUSDT', 'ISOLATED')

# order status: NEW, FILLED

# price = 2650
# overlap = price * Config.PRICE_OVERLAP
# order_purchase = Config.DEPOSIT / Config.ORDERS_GRID
# amount_purchase = getInitialPurchaseAmount(Config.DEPOSIT * Config.LEVERAGE * 0.999, Config.ORDERS_GRID, Config.MARTINGALE)
# price_change = overlap / (Config.ORDERS_GRID - 1)
# if Config.LOGARITHMIC:
#     price_change = price * getInitialPriceChange(Config.LOGARITHMIC_VALUE, Config.ORDERS_GRID, Config.PRICE_OVERLAP)

# purchases = []

# for _ in range(Config.ORDERS_GRID):
#     purchases.append(Buying(price, amount_purchase))
#     total_amount = sum([i.purchaseAmount for i in purchases])
#     print(f"price: {price}; amount: {amount_purchase}; profit: {total_amount * Config.PROFIT}")

#     if Config.LOGARITHMIC:
#         price -= price_change
#         price_change *= Config.LOGARITHMIC_VALUE
#     else:
#         price -= price_change

#     amount_purchase += amount_purchase * Config.MARTINGALE

# print(f"avgPrice: {avgPrice(purchases)}")
