from src.application.ports.page_loader import ResourceLoader
from src.domain.value_objects.uri import URI


class PageLoader:
    def __init__(
        self,
        loaders: dict[str, ResourceLoader],
    ):
        self._loaders = loaders

    def load(self, uri: URI):
        try:
            loader = self._loaders[uri.scheme]
        except KeyError as e:
            raise ValueError(f"No loader for scheme {uri.scheme}") from e

        return loader.load(uri)
