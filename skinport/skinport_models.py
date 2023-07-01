from typing import TypedDict, Dict


def format_usd(amount_usd: float) -> str:
    return '${:,.2f}'.format(amount_usd)


class SkinportJsonItem(TypedDict):
    market_hash_name: str
    currency: str
    suggested_price: float
    item_page: str
    market_page: str
    min_price: float
    max_price: float
    mean_price: float
    quantity: int
    created_at: int
    updated_at: int


class SkinportItem:
    def __init__(self, skinport_item_json: SkinportJsonItem):
        self.skinport_item_json = skinport_item_json

    @property
    def market_hash_name(self) -> str:
        return self.skinport_item_json.get('market_hash_name')

    @property
    def currency(self) -> str:
        return self.skinport_item_json.get('currency')

    @property
    def suggested_price(self) -> float:
        return self.skinport_item_json.get('suggested_price')

    @property
    def item_page(self) -> str:
        return self.skinport_item_json.get('item_page')

    @property
    def market_page(self) -> str:
        return self.skinport_item_json.get('market_page')

    @property
    def min_price(self) -> float:
        return self.skinport_item_json.get('min_price')

    @property
    def max_price(self) -> float:
        return self.skinport_item_json.get('max_price')

    @property
    def mean_price(self) -> float:
        return self.skinport_item_json.get('mean_price')

    @property
    def quantity(self) -> int:
        return self.skinport_item_json.get('quantity')

    @property
    def created_at(self) -> int:
        return self.skinport_item_json.get('created_at')

    @property
    def updated_at(self) -> int:
        return self.skinport_item_json.get('updated_at')


class SkinportEvent:
    def __init__(self, event_data: Dict) -> None:
        self.event_data = event_data
        self.sales = [SkinportEventItem(sale) for sale in self.event_data.get('sales')]

    @property
    def event_type(self) -> str:
        return self.event_data.get('eventType')


class SkinportEventItem:
    def __init__(self, sale_data: Dict) -> None:
        self.sale_data = sale_data

    @property
    def id(self) -> int:
        return self.sale_data.get('id')

    @property
    def sale_id(self) -> int:
        return self.sale_data.get('saleId')

    @property
    def product_id(self) -> int:
        return self.sale_data.get('productId')

    @property
    def assert_id(self) -> int:
        return self.sale_data.get('assetId')

    @property
    def item_id(self) -> int:
        return self.sale_data.get('itemId')

    @property
    def url(self) -> str:
        return self.sale_data.get('url')

    @property
    def full_url(self) -> str:
        return f'https://skinport.com/item/{self.url}/{self.sale_id}'

    @property
    def market_name(self) -> str:
        return self.sale_data.get('marketName')

    @property
    def market_hash_name(self) -> str:
        return self.sale_data.get('marketHashName')

    @property
    def suggested_price(self) -> int:
        return self.sale_data.get('suggestedPrice')

    @property
    def suggested_price_formatted(self) -> str:
        return format_usd(self.suggested_price / 100.0)

    @property
    def sale_price(self) -> int:
        return self.sale_data.get('salePrice')

    @property
    def sale_price_formatted(self) -> str:
        return format_usd(self.sale_price / 100.0)

    @property
    def currency(self) -> str:
        return self.sale_data.get('currency')

    @property
    def wear(self) -> float:
        return self.sale_data.get('wear')

    @property
    def exterior(self) -> str:
        return self.sale_data.get('exterior')

    @property
    def stattrak(self) -> bool:
        return self.sale_data.get('stattrak')

    @property
    def souvenir(self) -> str:
        return self.sale_data.get('souvenir')
