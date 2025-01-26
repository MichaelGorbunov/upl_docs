import os

import requests
from dotenv import load_dotenv

load_dotenv()


admin_tg_chat = os.getenv("TELEGRAM_ADMIN_CHAT")
tg_bot_url = os.getenv("TELEGRAM_BOT_URL")
tg_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


def send_telegram_message(chat_id, message):
    """
    Отправка сообщения в телеграм чат
    :param chat_id: id чата
    :param message: текст сообщения
    return:
    """
    params = {"chat_id": chat_id, "text": message}
    requests.post(
        f"{tg_bot_url}{tg_bot_token}/sendMessage",
        params=params,
    )


def print_message():
    print("Док загружен")


def send_message(message, chat_id=admin_tg_chat):
    # message="Загружен новый документ"

    send_telegram_message(chat_id, message)
