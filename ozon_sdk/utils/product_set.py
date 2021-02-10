from ..objects.product import BaseProduct
from typing import List
from ..exceptions import UnsupportedTypeException


class BaseProductSet:

    def __init__(self, base_products_list: List[BaseProduct]):
        if type(base_products_list) is not list:
            raise UnsupportedTypeException("base_products_list must be List of BaseProduct objects")
        for prod in base_products_list:
            if type(prod) is not BaseProduct:
                raise UnsupportedTypeException("base_products_list must be List of BaseProduct objects")
        self.base_products_list = base_products_list


class UpdatePriceStocksProductSet(BaseProductSet):
    pass


class ExportBaseProductSet(BaseProductSet):
    pass
