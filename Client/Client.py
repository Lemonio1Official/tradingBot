import hashlib
import hmac
import requests
from time import time
from typing import Dict, Any, Literal
from .Types import params, OrderParams

class Client:
    BASE_URL = "https://fapi.binance.com"

    def __init__(self, API_KEY: str, API_SECRET: str) -> None:
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def Balance(self, currency: str = "USDT"):
        endpoint = "/fapi/v2/balance"
        res = self.__Request('GET', endpoint).json()
        return next(filter(lambda i: i.get('asset') == currency, res), None)

    def Order(self, params: OrderParams, action: Literal['create', 'info', 'cancel'] = 'create'):
        endpoint = "/fapi/v1/order"
        method = 'POST' if action == 'create' else 'GET' if action == 'info' else 'DELETE'

        return self.__Request(method, endpoint, params.__dict__).json()

    def Leverage(self, symbol: str, leverage: int):
        endpoint = "/fapi/v1/leverage"
        params = {
            "symbol": symbol,
            "leverage": leverage
        }
        return self.__Request('POST', endpoint, params).json()

    def MarginType(self, symbol: str, type: Literal['ISOLATED', 'CROSSED']):
        endpoint = "/fapi/v1/marginType"
        params = {
            "symbol": symbol,
            "marginType": type
        }
        return self.__Request('POST', endpoint, params).json()

    def Check(self):
        url = 'https://api.binance.com/api/v3/account'
        params = { 'timestamp': int(time() * 1000) }
        params['signature'] = self.__GenerateSignature(params)
        headers = {'X-MBX-APIKEY': self.API_KEY}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise ValueError("Invalid API_KEY or SECRET_KEY")

    # STATIC
    @staticmethod
    def GetPrice(symbol: str):
        url = f'https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}'
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"getPrice error code: {response.status_code}")

        data = response.json()
        return float(data['price'])

    @staticmethod
    def GetSymbolInfo(symbol: str):
        url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
        response = requests.get(url)
        if response.status_code == 200:
            exchange_info = response.json()
            for i in exchange_info['symbols']:
                if i['symbol'] == symbol:
                    return i
        return None

    # PRIVATE
    def __Request(self, method: Literal["GET", "POST", "DELETE"], endpoint: str, params: params = {}) -> requests.Response:
        headers = { 'X-MBX-APIKEY': self.API_KEY }
        params['timeInForce'] = 'GTC'
        params['timestamp'] = int(time() * 1000)

        params = {key: value for key, value in params.items() if value is not None}
        params['signature'] = self.__GenerateSignature(params)

        return getattr(requests, method.lower())(self.BASE_URL + endpoint, headers=headers, params=params)

    def __GenerateSignature(self, params: params):
        query_string = '&'.join([f"{key}={params[key]}" for key in params])
        return hmac.new(self.API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
