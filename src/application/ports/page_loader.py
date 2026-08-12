from typing import Protocol

from src.domain.value_objects.uri import URI


class ResourceLoader(Protocol):
    def load(self, uri: URI) -> bytes: ...
