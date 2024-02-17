from typing import List

class Buying:
    price: float
    purchaseAmount: float

    def __init__(self, price: float, purchaseAmount: float) -> None:
        self.price = price
        self.purchaseAmount = purchaseAmount

def avgPrice(buys: List[Buying]):
    totalCost = totalProduct = 0
    for i in buys:
        totalCost += i.purchaseAmount
        totalProduct += i.purchaseAmount / i.price
    return totalCost / totalProduct

def getInitialPurchaseAmount(deposit: float, ordersGrid: int, martingale: float):
    x = 1
    total = 0
    for _ in range(ordersGrid):
        total += x
        x += x * martingale
    return deposit / total

def getInitialPriceChange(logarithmicValue: float, ordersGrid: int, priceOverlap: int):
    x = 1
    total = 0
    for _ in range(ordersGrid - 1):
        total += x
        x *= logarithmicValue
    return priceOverlap / total
