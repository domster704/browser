from src.application.ports.page_loader import ResourceLoader
from src.domain.entities.resource import Resource
from src.domain.value_objects.uri import URI
from src.infrastructure.http.cache import HTTPCache, CACHEABLE_STATUSES
from src.infrastructure.http.cache_control import parse_cache_control, CachePolicy
from src.infrastructure.http.client import HTTPClient
from src.infrastructure.http.request import HTTPRequest
from src.infrastructure.http.response import HTTPResponse
from src.infrastructure.types.http_methods import HTTPMethods


class HTTPResourceLoader(ResourceLoader):
    def __init__(
        self,
        client: HTTPClient,
        cache: HTTPCache | None = None,
    ):
        self.client = client
        self.cache = cache or HTTPCache()

    def load(self, uri: URI) -> Resource:
        request = HTTPRequest(uri)

        if request.method == HTTPMethods.GET:
            cache_response = self.cache.get(uri)
            if cache_response:
                print("Cache hit:", uri)
                return self._to_resource(cache_response)

        print(f"CACHE MISS: {uri}")

        request.add_headers(
            {
                "Host": uri.host,
                "Connection": "keep-alive",
                "User-Agent": "Test",
            }
        )
        response: HTTPResponse = self.client.send(request)

        cache_policy: CachePolicy = self._can_cache(request, response)
        if cache_policy.cacheable:
            self.cache.put(uri=uri, response=response, max_age=cache_policy.max_age)

        return self._to_resource(response)

    def _can_cache(self, request: HTTPRequest, response: HTTPResponse) -> CachePolicy:
        if request.method != HTTPMethods.GET:
            return False
        if response.status not in CACHEABLE_STATUSES:
            return False

        policy: CachePolicy = parse_cache_control(response.headers.get("cache-control"))
        return policy

    @staticmethod
    def _to_resource(response: HTTPResponse) -> Resource:
        return Resource(
            body=response.body,
            mime_type=response.mime_type,
            charset=response.charset,
        )
