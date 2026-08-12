from pprint import pprint

from src.application.service.page_loader import PageLoader
from src.domain.entities.html_document import HTMLDocument
from src.domain.html.tokenizer import HTMLTokenizer
from src.domain.value_objects.uri import URI
from src.infrastructure.adapters.data_resource_loader import DataResourceLoader
from src.infrastructure.adapters.file_resource_loader import FileResourceLoader
from src.infrastructure.adapters.http_resource_loader import HTTPResourceLoader
from src.infrastructure.http.socket_client import SocketHTTPClient

http_client = SocketHTTPClient()

page_loader = PageLoader(
    loaders={
        "http": HTTPResourceLoader(http_client),
        "https": HTTPResourceLoader(http_client),
        "file": FileResourceLoader(),
        "data": DataResourceLoader(),
    }
)

uri = URI.parse("file:///E:/ITSoft/Programming/vscode/index.html")
# uri = URI.parse("data:text/plain;base64," "SGVsbG8sIFdvcmxkIQ%3D%3D")

resource = page_loader.load(uri)
html = HTMLDocument(source=resource.decode())

html_tokenizer = HTMLTokenizer(document=html)
pprint(html_tokenizer.tokenize())
