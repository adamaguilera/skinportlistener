import asyncio

from notification.notification_service import notification_service
from skinport.errors import HTTPException
from skinport.skinport_client import SkinportClient
from skinport.skinport_models import SkinportItem


async def main():
    skinport_client = SkinportClient()
    try:
        all_items = await skinport_client.get_items()
        all_items.sort(key=lambda item: item.suggested_price or 0, reverse=True)
        highest_suggested_item: SkinportItem = all_items[0]
        print(f'Found most expensive suggested price as {highest_suggested_item.market_hash_name} at ${highest_suggested_item.suggested_price}')
        notification_service.push_message(f'Highest suggested price is {highest_suggested_item.market_hash_name} at ${highest_suggested_item.suggested_price}')
    except HTTPException as he:
        print(f'Caught exception {he.message}')
    await skinport_client.close()

asyncio.run(main())
