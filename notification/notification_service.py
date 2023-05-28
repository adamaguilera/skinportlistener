from typing import Optional

import requests
from dotenv import dotenv_values


class NotificationService:
    def __init__(self):
        self._config = dotenv_values('.env')
        self._token = self._config['TOKEN_ID']
        self.url = 'https://api.telegram.org/bot'

    def push_message(self, message: str, user_id: Optional[str] = None) -> None:
        if not user_id:
            user_id = self._config['USER_ID']

        params = {
            'chat_id': user_id,
            'text': message,
        }
        requests.get(f'{self.url}{self._token}/sendMessage', params=params)


notification_service = NotificationService()
