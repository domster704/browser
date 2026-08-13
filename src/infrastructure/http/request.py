from src.domain.value_objects.uri import URI
from src.infrastructure.types.http_methods import HTTPMethods


class HTTPRequest:
    def __init__(
        self,
        uri: URI,
        method: HTTPMethods = HTTPMethods.GET,
    ):
        self.uri = uri
        self.method = method
        self.headers: dict[str, str] = {}
        self.body: bytes = b""

    def add_header(self, key: str, value: str):
        self.headers[key] = value

    def add_headers(self, headers: dict[str, str], /):
        self.headers |= headers

    def set_body(self, body: bytes, /):
        self.body = body

    def to_bytes(self) -> bytes:
        request = f"GET {self.uri.path} HTTP/1.0\r\n"
        request += "\r\n".join(f"{key}: {value}" for key, value in self.headers.items())
        request += "\r\n\r\n"
        return request.encode("utf-8") + self.body

    def __repr__(self):
        return (
            f"{self.uri} == "
            f"{self.to_bytes().decode("utf-8").replace("\r\n", " | ")}"
        )
