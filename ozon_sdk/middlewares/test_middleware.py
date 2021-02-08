from .abstract import ResponseMiddleware
import requests


class TestMiddleware(ResponseMiddleware):

    def process_response(self) -> requests.Response:
        print(len(self.response.json()))
        return self.response