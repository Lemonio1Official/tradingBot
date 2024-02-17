import requests
import talib
import numpy as np

class Indicators:
    @staticmethod
    def RSI(SYMBOL: str, INTERVAL: str, LENGTH: int = 14, LIMIT: int = 300):
        url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}"
        try:
            res = requests.get(url).json()
            data = []
            for i in res:
                data.append(float(i[4]))
            data = np.array(data)
            return talib.RSI(data, LENGTH)[-1]
        except Exception as e:
            print(f"RSI error: {e}")
