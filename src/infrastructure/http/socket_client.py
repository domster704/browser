import gzip
import socket
import ssl
from dataclasses import dataclass
from io import BufferedReader

from src.infrastructure.http.client import HTTPClient
from src.infrastructure.http.request import HTTPRequest
from src.infrastructure.http.response import HTTPResponse


@dataclass
class Connection:
    socket: socket.socket
    reader: BufferedReader


ConnectionKey = tuple[str, str, int]  # (scheme, host, port)


class SocketHTTPClient(HTTPClient):
    MAX_REDIRECTS = 4

    def __init__(self):
        self._connections: dict[ConnectionKey, Connection] = {}

    def send(self, request: HTTPRequest) -> HTTPResponse:
        for _ in range(self.MAX_REDIRECTS):
            response = self.__send_once(request)
            if response.status not in {301, 302, 303, 307, 308}:
                return response

            location = response.headers.get("location")
            if not location:
                raise response

            request = self.__create_redirect_request(request, location)
            print(request)

        raise RuntimeError("Too many redirects")

    def __send_once(self, request: HTTPRequest) -> HTTPResponse:
        uri = request.uri
        if uri.scheme not in {"http", "https"}:
            raise ValueError(f"Unsupported scheme: {uri.scheme}")

        port = uri.port
        if port is None:
            port = 80 if uri.scheme == "http" else 443

        key: ConnectionKey = (uri.scheme, uri.host, port)
        connection: Connection | None = self._connections.get(key, None)
        if connection is None:
            connection = self.__create_connection(uri.host, port, uri.scheme)
            self._connections[key] = connection

        try:
            connection.socket.sendall(request.to_bytes())
            response, reusable = self.__parse_response(connection.reader)
        except (OSError, EOFError):
            self.__close_connection(key)
            raise

        if not reusable:
            self.__close_connection(key)

        return response

    def __create_redirect_request(
        self, request: HTTPRequest, location: str
    ) -> HTTPRequest:
        redirect_uri = request.uri.resolve(location)

        headers = request.headers.copy()
        headers["Host"] = redirect_uri.host

        new_request = HTTPRequest(method=request.method, uri=redirect_uri)
        new_request.add_headers(headers)
        new_request.set_body(request.body)

        return new_request

    def __parse_response(self, response: BufferedReader) -> tuple[HTTPResponse, str]:
        status_line_bytes: bytes = response.readline()
        if not status_line_bytes:
            raise EOFError("Server closed connection")

        status_line = status_line_bytes.decode("iso-8859-1").rstrip("\r\n")
        version, status, reason = status_line.split(" ", 2)

        response_headers: dict[str, str] = {}

        while True:
            line: bytes = response.readline()
            if not line:
                raise EOFError("Server closed connection while reading headers")
            if line == b"\r\n":
                break

            decoded: str = line.decode("iso-8859-1")

            header, value = decoded.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        content_length_header = response_headers.get("content-length", None)
        connection_header: str = response_headers.get("connection", "").casefold()
        reusable = False

        transfer_encoding = response_headers.get("transfer-encoding")
        content_encoding = response_headers.get("content-encoding")

        if transfer_encoding:
            encodings = [
                encoding.strip().casefold() for encoding in transfer_encoding.split(",")
            ]
            if encodings[-1] != "chunked":
                raise NotImplementedError(
                    f"Unsupported Transfer-Encoding: {transfer_encoding}"
                )
            body = self.__read_chunked_body(response)
        elif content_length_header is not None:
            content_length = int(content_length_header)
            body: bytes = response.read(content_length)
            if len(body) != content_length:
                raise EOFError(
                    f"Expected {content_length} bytes, got {len(body)} bytes"
                )

            if version == "HTTP/1.0":
                # В протоколе HTTP/1.0, если заголовок Content-Length отсутствует, конец передачи данных
                # определяется моментом разрыва TCP-соединения сервером. Клиент читает поток до тех пор,
                # пока сокет не вернет признак конца файла
                reusable = connection_header == "keep-alive"
            else:
                reusable = connection_header != "close"
        else:
            body = response.read()

        if content_encoding:
            encoding = content_encoding.casefold()
            if encoding == "gzip":
                body = gzip.decompress(body)
            else:
                raise NotImplementedError(f"Unknown Content-Encoding: {encoding!r}")

        return (
            HTTPResponse(
                version=version,
                status=int(status),
                reason=reason,
                headers=response_headers,
                body=body,
            ),
            reusable,
        )

    def __create_connection(self, host: str, port: int, scheme: str) -> Connection:
        sock: socket.socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )

        try:
            sock.connect((host, port))
            if scheme == "https":
                context: ssl.SSLContext = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=host)

            reader: BufferedReader = sock.makefile("rb")
            return Connection(
                socket=sock,
                reader=reader,
            )
        except Exception:
            sock.close()
            raise

    def __close_connection(self, key: ConnectionKey) -> None:
        connection = self._connections.pop(key, None)
        if connection is None:
            return

        try:
            connection.reader.close()
        finally:
            connection.socket.close()

    def __read_chunked_body(self, reader: BufferedReader) -> bytes:
        body = bytearray()

        while True:
            size_line: bytes = reader.readline()
            if not size_line:
                raise EOFError("Server closed connection while reading chunk size")
            size_line = size_line.rstrip(b"\r\n")

            size_text = size_line.split(b";", 1)[0]
            try:
                chunk_size = int(size_text, 16)
            except ValueError as e:
                raise ValueError(f"Invalid chunk size: {size_text}") from e

            if chunk_size == 0:
                self.__read_trailers(reader)
                break

            chunk = reader.read(chunk_size)
            if len(chunk) != chunk_size:
                raise EOFError(f"Expected {chunk_size} bytes, got {len(chunk)}")

            body.extend(chunk)
            ending = reader.read(2)  # \r\n
            if ending != b"\r\n":
                raise ValueError(f"Invalid chunk ending: {ending!r}")

        return bytes(body)

    def __read_trailers(self, reader: BufferedReader) -> None:
        while True:
            line = reader.readline()
            if not line:
                raise EOFError("Server closed connection while reading trailers")
            if line == b"\r\n":
                return
