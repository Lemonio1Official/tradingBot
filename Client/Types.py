from typing import Dict, Any, Literal, Optional

params = Dict[str, Any]

class OrderParams:
    symbol: Optional[str]
    side: Optional[Literal['BUY', 'SELL']]
    type: Optional[Literal['LIMIT', 'MARKET', 'STOP', 'TAKE_PROFIT', 'STOP_MARKET', 'TAKE_PROFIT_MARKET']]
    quantity: Optional[float]
    price: Optional[float]
    stopPrice: Optional[float] # Used with STOP/STOP_MARKET or TAKE_PROFIT/TAKE_PROFIT_MARKET orders
    closePosition: Optional[Literal['true', 'false']]
    orderId: Optional[str]

    # Type	Additional mandatory parameters
    # LIMIT	timeInForce, quantity, price
    # MARKET	quantity
    # STOP/TAKE_PROFIT	quantity, price, stopPrice
    # STOP_MARKET/TAKE_PROFIT_MARKET	stopPrice
    # TRAILING_STOP_MARKET	callbackRate

    def __init__(self, symbol: Optional[str] = None, side: Optional[Literal['BUY', 'SELL']] = None, type: Optional[Literal['LIMIT', 'MARKET', 'STOP', 'TAKE_PROFIT', 'STOP_MARKET', 'TAKE_PROFIT_MARKET']] = None, quantity: Optional[float] = None, price: Optional[float] = None, stopPrice: Optional[float] = None, closePosition: Optional[Literal['true', 'false']] = None, orderId: Optional[str] = None):
        self.symbol = symbol
        self.side = side
        self.type = type
        self.quantity = quantity
        self.price = price
        self.stopPrice = stopPrice
        self.closePosition = closePosition
        self.orderId = orderId
