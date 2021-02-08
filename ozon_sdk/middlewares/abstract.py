import requests
from abc import ABC, abstractmethod


class ResponseMiddleware:

    def __init__(self, response: requests.Response):
        self.response = response

    @abstractmethod
    def process_response(self) -> requests.Response:
        """

        :return: requests.Response
        """
        return self.response
