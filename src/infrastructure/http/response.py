class HTTPResponse:
    def __init__(
        self,
        version: str,
        status: int,
        reason: str,
        headers: dict[str, str],
        body: bytes,
    ):
        self.version = version
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body
