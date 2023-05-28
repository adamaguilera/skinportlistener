from typing import TypedDict


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


