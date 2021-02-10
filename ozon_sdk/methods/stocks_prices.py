from ..objects.product import BaseProduct
from typing import List
from ..utils import RequestMachine
from ..request import GetPricesRequestV1
from ..request import GetStocksRequestV1


def _clean_price_stock_responses(responses_list) -> List[dict]:
    output = []
    for response in responses_list:
        output += response["result"]['items']
    return output


def _transform_price_stock_data_to_obj(stock_dict_items: List[dict], price_dict_items: List[dict]) -> List[BaseProduct]:
    """
    Function transforms Ozon JSON items to validated Product objects.
    :param stock_dict_items: example [{"offer_id": "", "product_id": "", "stock": {"present": 0, ...}}, ...]
    :param price_dict_items: example [{"offer_id": "", "product_id": "", "price": {"price": 1000.00, ...}}, ...]
    :return: List[Product]
    """
    output_products = []

    # Matching both of lists by offer_id
    stocks_dict = {
        el["offer_id"]: el for el in stock_dict_items
    }
    prices_dict = {
        el["offer_id"]: el for el in price_dict_items
    }
    # Fill empty dict with all keys(offer_id's)
    matching_dict = {}
    for el in stocks_dict:
        matching_dict[el] = {}
    for el in prices_dict:
        matching_dict[el] = {}
    # Fill dict values
    for el in matching_dict:
        try:
            matching_dict[el].update(stocks_dict[el])
        except:
            pass
        try:
            matching_dict[el].update(prices_dict[el])
        except:
            pass
    # Create and fill objects.
    for key, value in matching_dict.items():
        new_product = BaseProduct()
        new_product.fill_from_response_item(value)
        output_products.append(new_product)
    return output_products


def get_base_products(client_id: str,
                      api_key: str,
                      products_in_chunk: int = 1000,
                      downloading_threads_max_count: int = 2,
                      with_stocks: bool = True,
                      with_prices: bool = True) -> List[BaseProduct]:
    """
    Function collects from Ozon API products with basic info like a prices, stocks, commissions.
    :param client_id: Client Id from own cabinet
    :param api_key: Api Key from own cabinet
    :param products_in_chunk: products count per page(Max=1000). How many items we can collect by 1 request.
    :param downloading_threads_max_count: How many threads we can use for collecting.
    (Ozon doesn't interested in much requests per minute)
    :param with_stocks: Returning products will be contains stocks data. Else None for stocks parameters.
    :param with_prices: Returning products will be contains prices and commissions data. Else None for prices parameters
    :return: List of Validated BaseProduct objects.
    """
    # Find total products and pages count
    request = GetStocksRequestV1(client_id, api_key, 1, 10)
    result = request.get_result()
    total_products_count = int(result["result"]["total"])
    total_pages_count = total_products_count // products_in_chunk + 1
    # Set default values for responses
    stock_responses = []
    price_responses = []
    # Get stocks data
    if with_stocks:
        stocks_requests_pool = [
            GetStocksRequestV1(client_id, api_key, page, products_in_chunk) for page in range(1, total_pages_count + 1)
        ]
        stocks_machine = RequestMachine(stocks_requests_pool, downloading_threads_max_count)
        stock_responses = stocks_machine.get_results()
    # Get prices data
    if with_prices:
        prices_requests_pool = [
            GetPricesRequestV1(client_id, api_key, page, products_in_chunk) for page in range(1, total_pages_count + 1)
        ]
        prices_machine = RequestMachine(prices_requests_pool, downloading_threads_max_count)
        price_responses = prices_machine.get_results()
    # Transform data to output objects.
    objects = _transform_price_stock_data_to_obj(
        stock_dict_items=_clean_price_stock_responses(stock_responses),
        price_dict_items=_clean_price_stock_responses(price_responses)
    )
    return objects


