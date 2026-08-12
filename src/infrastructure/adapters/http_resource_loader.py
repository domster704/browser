from src.application.ports.http_client import HTTPClient
from src.application.ports.page_loader import ResourceLoader
from src.domain.value_objects.uri import URI
from src.infrastructure.http.request import HTTPRequest
from src.infrastructure.http.response import HTTPResponse


class HTTPResourceLoader(ResourceLoader):
    def __init__(
        self,
        client: HTTPClient,
    ):
        self.client = client

    def load(self, uri: URI) -> bytes:
        request = HTTPRequest(uri)

        request.add_headers(
            headers={
                "Host": uri.host,
                "Connection": "close",
                "User-Agent": "Test",
            }
        )

        response: HTTPResponse = self.client.send(request)

        return response.body
