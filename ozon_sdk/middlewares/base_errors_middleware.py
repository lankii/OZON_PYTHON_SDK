from .abstract import ResponseMiddleware
from ..exceptions import Response403Exception
import requests


class BaseErrorsMiddleware(ResponseMiddleware):

    def _process_status_code(self):
        if self.response.status_code == 403:
            raise Response403Exception(f"Unauthorized. "
                                       f"Code: {self.response.json()['error']['code']}. "
                                       f"Message: {self.response.json()['error']['message']}")

    def process_response(self) -> requests.Response:
        self._process_status_code()
        return self.response
