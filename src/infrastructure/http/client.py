from typing import Protocol

from src.infrastructure.http.request import HTTPRequest
from src.infrastructure.http.response import HTTPResponse


class HTTPClient(Protocol):
    def send(self, request: HTTPRequest) -> HTTPResponse: ...
