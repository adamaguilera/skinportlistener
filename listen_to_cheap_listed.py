from skinport.skinport_client import SkinportClient
from skinport.skinport_models import SkinportEvent
from notification.notification_service import notification_service

skinport_client = SkinportClient()


@skinport_client.listen("saleFeed")
async def on_sale_feed(data):
    # convert data to easy parse
    sale_event_data = SkinportEvent(data)
    if sale_event_data.event_type != 'listed':
        return
    for sale in sale_event_data.sales:
        if sale.sale_price < sale.suggested_price:
            message = f'Caught listing for {sale.market_hash_name} at ${sale.sale_price/100.0} with suggested ${sale.suggested_price/100.0}. Find this listing here {sale.full_url}'
            print(message)
            notification_service.push_message(message=message)


skinport_client.run()
