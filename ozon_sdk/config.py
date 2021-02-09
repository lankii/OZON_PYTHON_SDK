from .middlewares.abstract import ResponseMiddleware
from .middlewares import BaseErrorsMiddleware

from typing import List, Type


BASE_URL = "http://api-seller.ozon.ru"

MIDDLEWARE: List[Type[ResponseMiddleware]] = [
    BaseErrorsMiddleware
]