import requests

from config.secrets import secrets


def send_message_to_telegram(message_in_html):
    base_url = f'https://api.telegram.org/bot{secrets["TELEGRAM_BOT_TOKEN"]}/sendMessage'
    data = {
        "chat_id": secrets["TELEGRAM_CHAT_ID"],
        "parse_mode": "HTML",
        "text": message_in_html
    }
    response = requests.post(base_url, data=data)
