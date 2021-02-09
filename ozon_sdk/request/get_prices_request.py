from .get_stocks_request import GetStocksRequestV1


class GetPricesRequestV1(GetStocksRequestV1):

    URI = "/v1/product/info/prices"
