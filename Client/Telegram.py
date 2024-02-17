import telebot
from config import Config
from env import TG_TOKEN

class Telegram:
    bot = telebot.TeleBot(TG_TOKEN)

    @bot.message_handler(commands=['start'])
    def StartHandler(message):
        chat_id = message.chat.id
        print(chat_id)

    @staticmethod
    def SendMessage(text: str):
        Telegram.bot.send_message("1590871040", text)

    @staticmethod
    def DealDetails(currentOrder: int, amount: float, avgPrice: float):
        Telegram.SendMessage(
f"""🎯 {Config.TRADING_PAIR}\n\n{currentOrder} out of {Config.ORDERS_GRID} orders has been completed\n
Amount: {amount} {Config.TRADING_PAIR.replace('USDT', '')}
Par value: {round(avgPrice * amount, 2)} USDT
Average price: {avgPrice} USDT""".replace("\t", "")
        )

    @staticmethod
    def ProfitMessage(currentOrder: int, amount: float):
        Telegram.SendMessage(
f"""🚀 {Config.TRADING_PAIR}\n\n{currentOrder} out of {Config.ORDERS_GRID} orders has been completed\n
Revenue (USDT): {round(amount * Config.PROFIT, 4)}
"""
        )

    def start():
        Telegram.bot.polling()
