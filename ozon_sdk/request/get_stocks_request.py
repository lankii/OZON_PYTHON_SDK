from .abstract import Request, List, Union


class GetStocksRequestV1(Request):

    URI = "/v1/product/info/stocks"

    def __init__(self, client_id: str, api_key: str, page: int, page_size: int):
        super().__init__(client_id, api_key)
        self.page = page
        self.page_size = page_size

    @property
    def json_payload(self):
        return {
            "page": self.page,
            "page_size": self.page_size
        }

    def get_result(self) -> Union[dict, List[dict]]:
        response = self._post(self.URI, self.json_payload)
        return response.json()