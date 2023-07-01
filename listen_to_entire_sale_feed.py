from skinport.skinport_client import SkinportClient

skinport_client = SkinportClient()


@skinport_client.listen("saleFeed")
async def on_sale_feed(data):
    print(data)


skinport_client.run()
