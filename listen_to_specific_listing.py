from typing import List

from skinport.skinport_client import SkinportClient
from skinport.skinport_models import SkinportEvent, SkinportEventItem
from notification.notification_service import notification_service

skinport_client = SkinportClient()

match_from_list: List[List[str]] = [
    ['karambit', 'doppler'],
    ['bayonet', 'tiger', 'tooth']
]


async def item_matches(item: SkinportEventItem, filter_list: List[str]) -> bool:
    for filter_text in filter_list:
        if filter_text == 'stattrak' and not item.stattrak:
            return False
        elif filter_text not in item.url:
            return False
    return True


@skinport_client.listen("saleFeed")
async def on_sale_feed(data):
    # convert data to easy parse
    sale_event_data = SkinportEvent(data)
    if sale_event_data.event_type != 'listed':
        return
    for sale in sale_event_data.sales:
        for filter_item in match_from_list:
            if await item_matches(sale, filter_item):
                message = f'Caught listing for {sale.market_hash_name} at ${sale.sale_price_formatted} with suggested ${sale.suggested_price_formatted}. Find this listing here {sale.full_url}'
                print(message)
                notification_service.push_message(message=message)


skinport_client.run()
