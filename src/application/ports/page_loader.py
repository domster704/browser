from typing import Protocol

from src.domain.value_objects.uri import URI
from src.domain.entities.resource import Resource


class ResourceLoader(Protocol):
    def load(self, uri: URI) -> Resource: ...
