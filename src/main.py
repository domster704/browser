from pprint import pprint

from src.application.service.page_loader import PageLoader
from src.application.service.view_source_resource_loader import ViewSourceResourceLoader
from src.domain.html.document import HTMLDocument
from src.domain.html.dom.element_factory import HTMLElementFactory
from src.domain.html.dom.tree_builder import HTMLTreeBuilder
from src.domain.html.tokenizer.tokenizer import HTMLTokenizer
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
page_loader.register("view-source", ViewSourceResourceLoader(page_loader))

# uri = URI.parse("view-source:file:///E:/ITSoft/Programming/vscode/index.html")
uri = URI.parse("file:///E:/ITSoft/Programming/vscode/index.html")
# uri = URI.parse("view-source:https://google.com")
# uri = URI.parse("data:text/plain;base64," "SGVsbG8sIFdvcmxkIQ%3D%3D")

resource = page_loader.load(uri)
if uri.scheme == "view-source":
    print(resource.decode())
else:
    html = HTMLDocument(source=resource.decode())
    html_tokenizer = HTMLTokenizer(document=html)

    tokens = html_tokenizer.tokenize()

    html_builder = HTMLTreeBuilder(element_factory=HTMLElementFactory())
    pprint(html_builder.parse(tokens), width=200)
