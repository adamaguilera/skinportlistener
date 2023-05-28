import asyncio
import signal
from typing import List, Coroutine, Any

import socketio
from dotenv import dotenv_values

from skinport.http_client import HttpClient
from skinport.skinport_models import SkinportItem


class SkinportClient:
    def __init__(self):
        self._config = dotenv_values('.env')
        self._client_id = self._config['CLIENT_ID']
        self._client_secret = self._config['CLIENT_SECRET']
        self.http_client = HttpClient()
        self.websocket: socketio.AsyncClient = socketio.AsyncClient(logger=True, engineio_logger=True)
        self.connected = True

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
            loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())
        except NotImplementedError:
            pass

        async def runner():
            try:
                await self.connect()
            finally:
                if self.connected:
                    await self.close()

        def stop_loop_on_completion(f):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('Signal to terminate event listener')
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            print('Clean up tasks')

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                pass

    async def catch_all(self, event, data):
        print(f'Received event {event}')

    async def on_connect(self) -> None:
        print('Connected to skinport. Emitting saleFeedJoinEvent')
        await self.emit_sale_feed_join()

    async def connect(self) -> None:
        if self.connected:
            await self.close()

        try:
            self.websocket.on("*", self.catch_all)
            self.websocket.on('connect', lambda: asyncio.ensure_future(self.on_connect()))
            await self.websocket.connect("https://skinport.com", transports=['websocket'])
            self.connected = True
            await self.websocket.wait()
        except asyncio.TimeoutError:
            print('Connection timed out')
            await self.close()
            self.connected = False

    async def close(self) -> None:
        if not self.connected:
            return
        self.connected = False
        if self.websocket.eio.http is not None:
            await self.websocket.eio.http.close()
        await self.http_client.close()

    async def emit_sale_feed_join(self) -> None:
        await self.websocket.emit(
            'saleFeedJoin', {
                'currency': 'USD',
                'locale': 'en',
                'appid': '730',
            }
        )
        await self.websocket.wait()

    def listen(self, name: str = None) -> Coroutine[Any, Any, Any]:
        def decorator(f):
            if not asyncio.iscoroutinefunction(f):
                raise TypeError("Event listener must be a coroutine function")
            self.websocket.on(name, f)
            print(f'{f.__name__} has been registered as an event')
            return f
        return decorator

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
