from src.application.ports.page_loader import ResourceLoader
from src.application.service.page_loader import PageLoader
from src.domain.entities.resource import Resource
from src.domain.value_objects.uri import URI


class ViewSourceResourceLoader(ResourceLoader):
    def __init__(self, page_loader: PageLoader):
        self._page_loader = page_loader

    def load(self, uri: URI) -> Resource:
        inner_uri = URI.parse(uri.path)
        resource = self._page_loader.load(inner_uri)

        return Resource(
            body=resource.body,
            mime_type=resource.mime_type,
            charset=resource.charset,
        )
