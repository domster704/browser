from src.application.service.page_loader import PageLoader
from src.domain.value_objects.uri import URI
from src.infrastructure.adapters.file_resource_loader import FileResourceLoader
from src.infrastructure.adapters.http_resource_loader import HTTPResourceLoader
from src.infrastructure.http.socket_client import SocketHTTPClient

http_client = SocketHTTPClient()

page_loader = PageLoader(
    loaders={
        "http": HTTPResourceLoader(http_client),
        "https": HTTPResourceLoader(http_client),
        "file": FileResourceLoader(),
    }
)

uri = URI.parse(
    "file:///E:/ITSoft/Programming/vscode/index.html"
)

content = page_loader.load(uri)

print(content.decode("utf-8"))
