from .middlewares.abstract import ResponseMiddleware
from .middlewares.test_middleware import TestMiddleware

from typing import List, Type


BASE_URL = "http://api-seller.ozon.ru"

MIDDLEWARE: List[Type[ResponseMiddleware]] = [
    TestMiddleware
]