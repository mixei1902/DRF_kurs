import requests

from config.settings import TELEGRAM_URL, TELEGRAM_TOKEN


def send_telegram_message(chat_id, message):
    url = f"{TELEGRAM_URL}{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=data)
