import requests
from abc import ABC, abstractmethod
import os
from typing import List, Union
from ..config import BASE_URL
from ..config import MIDDLEWARE


class Request(ABC):
    """
    Abstract instance for Request to Ozon
    """
    _BASE_URL = BASE_URL

    def __init__(self, client_id: str, api_key: str):
        """
        Class constructor
        :param client_id: str - Client Id from own cabinet
        :param api_key: str - Api Key from own cabinet
        """
        self.client_id = client_id
        self.api_key = api_key

    @property
    def _headers(self):
        return {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def __get_full_url(self, uri):
        return f"{self._BASE_URL}{uri}"

    @staticmethod
    def __process_with_middleware(response):
        local_response = response
        for middleware in MIDDLEWARE:
            local_response = middleware(response).process_response()
        return local_response

    def _get(self, uri: str) -> requests.Response:
        """
        GET Request to Ozon API.
        :param uri: str - Request uri
        :return: Clean Response from 'requests' library.
        """
        response = requests.get(url=self.__get_full_url(uri),
                                headers=self._headers)
        return self.__process_with_middleware(response)

    def _post(self, uri: str, data: Union[dict, List[dict]]) -> requests.Response:
        """
        POST Request to Ozon API.
        :param uri: str - Request uri
        :param data: JSON serializable object. Can be Dict or List.
        :return: Clean Response from 'requests' library.
        """
        response = requests.post(url=self.__get_full_url(uri),
                                 headers=self._headers,
                                 json=data)
        return self.__process_with_middleware(response)

    @abstractmethod
    def get_result(self) -> Union[dict, List[dict]]:
        """
        This method must be implemented in child classes.
        :return: Final information from response. JSON serializable object. Can be Dict or List.
        """