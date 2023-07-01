from notification.notification_service import notification_service
from skinport.skinport_client import SkinportClient
from skinport.skinport_models import SkinportEvent

skinport_client = SkinportClient()


MINIMUM_SALE_PRICE_CENTS = 1000
DISCOUNT_PERCENTAGE = 1.0


@skinport_client.listen("saleFeed")
async def on_sale_feed(data):
    # convert data to easy parse
    sale_event_data = SkinportEvent(data)
    if sale_event_data.event_type != 'listed':
        return
    for sale_item in sale_event_data.sales:
        if (sale_item.suggested_price * DISCOUNT_PERCENTAGE) >= sale_item.sale_price >= MINIMUM_SALE_PRICE_CENTS:
            message = f'Caught discounted listing for {sale_item.market_hash_name} at {sale_item.sale_price_formatted} with a suggested price of {sale_item.suggested_price_formatted}. Find this listing here {sale_item.full_url}'
            notification_service.push_message(message)
            print(message)


skinport_client.run()
