from dataclasses import dataclass
from time import monotonic

from src.domain.value_objects.uri import URI
from src.infrastructure.http.response import HTTPResponse

CACHEABLE_STATUSES = {
    200,
    301,
    404,
}


@dataclass(frozen=True, slots=True)
class CacheEntry:
    response: HTTPResponse
    stored_at: float
    max_age: int | None

    @property
    def is_fresh(self) -> bool:
        if self.max_age is None:
            return True

        age = monotonic() - self.stored_at
        return age <= self.max_age


class HTTPCache:
    def __init__(self):
        self._entries: dict[URI, CacheEntry] = {}

    def get(self, uri: URI) -> HTTPResponse | None:
        entry: CacheEntry | None = self._entries.get(uri)
        if entry is None:
            return None

        if not entry.is_fresh:
            del self._entries[uri]
            return None

        return entry.response

    def put(self, uri: URI, response: HTTPResponse, max_age: int | None) -> None:
        self._entries[uri] = CacheEntry(
            response=response, stored_at=monotonic(), max_age=max_age
        )
