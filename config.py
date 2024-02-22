class Config:
    SIDE = 'SELL' # BUY/SELL
    TRADING_PAIR = 'ETHUSDT'
    DEPOSIT = 100 # int
    LEVERAGE = 10 # int 0 - 100
    PRICE_OVERLAP = 0.25 # float %
    ORDERS_GRID = 7 # int
    MARTINGALE = 0.07 # float %
    PROFIT = 0.0085 # float %
    LOGARITHMIC = True # bool ЛОГАРИФМІЧНИЙ РОЗПОДІЛ ЦІН вкл/викл
    LOGARITHMIC_VALUE = 1.05 # float ЛОГАРИФМІЧНИЙ РОЗПОДІЛ ЦІН
    FILTERS = [
        {'filter': 'RSI', 'interval': '1m', 'value': 40+30},
        {'filter': 'RSI', 'interval': '5m', 'value': 45+30},
        {'filter': 'RSI', 'interval': '15m', 'value': 50+30},
    ]
