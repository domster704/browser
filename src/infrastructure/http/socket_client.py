import socket
import ssl
from io import BufferedReader

from src.infrastructure.http.client import HTTPClient
from src.infrastructure.http.request import HTTPRequest
from src.infrastructure.http.response import HTTPResponse


class SocketHTTPClient(HTTPClient):
    def send(self, request: HTTPRequest) -> HTTPResponse:
        uri = request.uri
        if uri.scheme not in {"http", "https"}:
            raise ValueError(f"Unsupported scheme: {uri.scheme}")

        port = uri.port
        if port is None:
            port = 80 if uri.scheme == "http" else 443

        sock: socket.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )

        try:
            sock.connect((uri.host, uri.port))

            if uri.scheme == "https":
                context: ssl.SSLContext = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=uri.host)

            sock.sendall(request)
            raw_response: BufferedReader = sock.makefile("rb")
            try:
                return self.__parse_response(raw_response)
            finally:
                raw_response.close()
        finally:
            sock.close()

    def __parse_response(self, response: BufferedReader) -> HTTPResponse:
        status_line = response.readline().decode("iso-8859-1")
        version, status, reason = status_line.split(" ", 2)

        response_headers: dict[str, str] = {}

        while True:
            line: bytes = response.readline()
            if line == b"\r\n":
                break
            decoded: str = line.decode("iso-8859-1")

            header, value = decoded.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        body = response.read()
        return HTTPResponse(
            version=version,
            status=int(status),
            reason=reason,
            headers=response_headers,
            body=body,
        )
