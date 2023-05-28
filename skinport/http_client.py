from typing import Optional, Dict, Any

import aiohttp
from dotenv import dotenv_values

from skinport.errors import HTTPException


class HttpClient:
    def __init__(
            self,
    ) -> None:
        self.base_url = "https://api.skinport.com/v1/"
        self._config = dotenv_values('.env')
        self._session = aiohttp.ClientSession()
        self.user_agent = 'skinportlistener'
        self.auth = aiohttp.BasicAuth(login=self._config['CLIENT_ID'], password=self._config['CLIENT_SECRET'])

    async def close(self) -> None:
        await self._session.close()

    async def get_request(
            self,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        headers = {
            'User-Agent': self.user_agent,
        }
        kwargs['headers'] = headers
        kwargs['params'] = params

        async with self._session.request("GET", f'{self.base_url}{url}', auth=self.auth, **kwargs) as response:
            print(f"Request {url} has returned with {response.status}")

            data = await response.json()

            if 300 > response.status >= 200:
                return data

            raise HTTPException(status_code=response.status, data=data)
