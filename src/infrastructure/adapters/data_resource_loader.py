import base64
from urllib.parse import unquote_to_bytes

from src.application.ports.page_loader import ResourceLoader
from src.domain.value_objects.uri import URI
from src.domain.entities.resource import Resource


class DataResourceLoader(ResourceLoader):
    """
    data:[<media-type>][;charset=<charset>][;base64],<data>

    Examples:
        data:text/html;charset=utf-8,<h1>Hello</h1>
        data:text/plain,Hello%20world
        data:image/png;base64,iVBORw0KGgo...
        data:,Hello
    """

    def load(self, uri: URI) -> Resource:
        if uri.scheme != "data":
            raise ValueError(f"Expected data URI, got {uri.scheme} URI")

        metadata, encoded_data = uri.path.split(",", 1)

        metadata_parts: list[str] = metadata.split(";")
        mime_type = metadata_parts[0] or "text/plain"

        charset: str | None = None
        is_base64 = False

        for parameter in metadata_parts[1:]:
            if parameter.casefold() == "base64":
                is_base64 = True
                continue

            key, separator, value = parameter.partition("=")
            if separator and key.casefold() == "charset":
                charset = value

        if mime_type == "text/plain" and charset is None:
            charset = "US-ASCII"

        decoded_data: bytes = unquote_to_bytes(encoded_data)
        if is_base64:
            body: bytes = base64.b64decode(decoded_data)
        else:
            body: bytes = decoded_data

        return Resource(
            body=body,
            mime_type=mime_type,
            charset=charset,
        )
