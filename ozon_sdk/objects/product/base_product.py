from typing import List


class ProductCommission:
    """

    """
    percent: int = None
    min_value: float = None
    value: float = None
    sale_schema: str = None
    delivery_amount: float = None
    return_amount: float = None

    def fill_from_price_item(self, commission_dict: dict):
        for key, value in commission_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self


class Product:
    """

    """
    product_id: int = None
    offer_id: str = None
    stock_coming: int = None
    stock_present: int = None
    stock_reserved: int = None
    price: float = None
    old_price: float = None
    premium_price: float = None
    recommended_price: float = None
    retail_price: float = None
    vat: float = None
    buybox_price: float = None
    min_ozon_price: float = None
    marketing_price: float = None
    marketing_seller_priced: float = None
    marketing_actions: str = None
    volume_weight: float = None
    commissions: List[ProductCommission] = []

    def fill_from_response_item(self, response_item: dict):
        self.product_id = response_item.get("product_id", self.product_id)
        self.offer_id = response_item.get("offer_id", self.offer_id)
        stock_data = response_item.get("stock", None)
        if stock_data:
            self.stock_coming = int(stock_data.get("coming", 0))
            self.stock_present = int(stock_data.get("present", 0))
            self.stock_reserved = int(stock_data.get("reserved", 0))
        price_data = response_item.get("price", None)
        if price_data:
            try:
                self.price = float(price_data.get("price", 0))
            except:
                self.price = 0
            try:
                self.old_price = float(price_data.get("old_price", 0))
            except:
                self.old_price = 0
            try:
                self.premium_price = float(price_data.get("premium_price", 0))
            except:
                self.premium_price = 0
            try:
                self.recommended_price = float(price_data.get("recommended_price", 0))
            except:
                self.recommended_price = 0
            try:
                self.retail_price = float(price_data.get("retail_price", 0))
            except:
                self.retail_price = 0
            try:
                self.vat = float(price_data.get("vat", 0))
            except:
                self.vat = 0
            try:
                self.buybox_price = float(price_data.get("buybox_price", 0))
            except:
                self.buybox_price = 0
            try:
                self.min_ozon_price = float(price_data.get("min_ozon_price", 0))
            except:
                self.min_ozon_price = 0
            try:
                self.marketing_price = float(price_data.get("marketing_price", 0))
            except:
                self.marketing_price = 0
            try:
                self.marketing_seller_price = float(price_data.get("marketing_seller_price", 0))
            except:
                self.marketing_seller_price = 0

            try:
                self.price_index = float(response_item.get("price_index", 0))
            except:
                self.price_index = 0

            commissions = response_item.get("commissions", None)
            if commissions:
                self.commissions = [ProductCommission().fill_from_price_item(item) for item in commissions]
        return self