from typing import List

from dotenv import dotenv_values

from skinport.http_client import HttpClient
from skinport.skinport_models import SkinportItem


class SkinportClient:
    def __init__(self):
        self._config = dotenv_values('.env')
        self._client_id = self._config['CLIENT_ID']
        self._client_secret = self._config['CLIENT_SECRET']
        self.http_client = HttpClient()

    async def close(self) -> None:
        await self.http_client.close()

    async def get_items(
            self,
            app_id: str = '730',
            currency: str = 'USD',
            tradable: bool = False,
    ) -> List[SkinportItem]:
        params = {
            'app_id': app_id,
            'currency': currency,
            'tradable': str(tradable).lower(),
        }
        data = await self.http_client.get_request(url="items", params=params)
        return [SkinportItem(item) for item in data]
