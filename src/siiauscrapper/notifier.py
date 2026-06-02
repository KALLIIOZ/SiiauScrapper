import requests
from typing import Iterable

from .settings import TELEGRAM_BOT_TOKEN


class TelegramNotifier:
    def __init__(self, token: str = None): # type: ignore
        self.token = token or TELEGRAM_BOT_TOKEN
        self.endpoint = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str, chat_ids: Iterable[int]) -> None:
        for chat_id in chat_ids:
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            try:
                response = requests.post(self.endpoint, json=payload, timeout=10)
                response.raise_for_status()
                print(f"Mensaje enviado a {chat_id}.")
            except requests.RequestException as exc:
                print(f"Error enviando mensaje a {chat_id}: {exc}")
