from pathlib import Path
from urllib.request import url2pathname

from src.application.ports.page_loader import ResourceLoader
from src.domain.value_objects.uri import URI


class FileResourceLoader(ResourceLoader):
    def load(self, uri: URI) -> bytes:
        if uri.scheme != "file":
            raise ValueError(f"File loader cannot load {uri.scheme!r}")

        if uri.host not in {None, "", "localhost"}:
            raise ValueError(f"Remote file hosts are not supported: {uri.host}")

        path = Path(url2pathname(uri.path))
        return path.read_bytes()
