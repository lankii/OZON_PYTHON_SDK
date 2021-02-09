from ..objects.product import Product
from typing import List
from ..utils import RequestMachine
from ..request import GetPricesRequestV1
from ..request import GetStocksRequestV1


def _clean_price_stock_responses(responses_list) -> List[dict]:
    output = []
    for response in responses_list:
        output += response["result"]['items']
    return output


def _transform_price_stock_data_to_obj(stock_dict_items: List[dict], price_dict_items: List[dict]) -> List[Product]:

    output_products = []

    # Matching both of lists by offer_id
    stocks_dict = {
        el["offer_id"]: el for el in stock_dict_items
    }
    prices_dict = {
        el["offer_id"]: el for el in price_dict_items
    }

    matching_dict = {}
    for el in stocks_dict:
        matching_dict[el] = {}
    for el in prices_dict:
        matching_dict[el] = {}

    for el in matching_dict:
        try:
            matching_dict[el].update(stocks_dict[el])
        except:
            pass
        try:
            matching_dict[el].update(prices_dict[el])
        except:
            pass

    for key, value in matching_dict.items():
        new_product = Product()
        new_product.fill_from_response_item(value)
        output_products.append(new_product)
    return output_products


def get_products(client_id: str,
                 api_key: str,
                 products_in_chunk: int = 1000,
                 downloading_threads_max_count: int = 2,
                 with_stocks: bool = True,
                 with_prices: bool = True) -> List[Product]:

    # Find total products count
    request = GetStocksRequestV1(client_id, api_key, 1, 10)
    result = request.get_result()
    total_products_count = int(result["result"]["total"])
    total_pages_count = total_products_count // products_in_chunk + 1
    stock_responses = []
    price_responses = []

    if with_stocks:
        stocks_requests_pool = [
            GetStocksRequestV1(client_id, api_key, page, products_in_chunk) for page in range(1, total_pages_count + 1)
        ]
        stocks_machine = RequestMachine(stocks_requests_pool, downloading_threads_max_count)
        stock_responses = stocks_machine.get_results()

    if with_prices:
        prices_requests_pool = [
            GetPricesRequestV1(client_id, api_key, page, products_in_chunk) for page in range(1, total_pages_count + 1)
        ]
        prices_machine = RequestMachine(prices_requests_pool, downloading_threads_max_count)
        price_responses = prices_machine.get_results()

    objects = _transform_price_stock_data_to_obj(
        stock_dict_items=_clean_price_stock_responses(stock_responses),
        price_dict_items=_clean_price_stock_responses(price_responses)
    )

    return objects


