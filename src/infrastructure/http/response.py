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

        self.mime_type, self.charset = self.__parse_content_type()

    def __parse_content_type(self) -> tuple[str | None, str | None]:
        content_type: str | None = self.headers.get("content-type")

        if content_type is None:
            return None, None

        parts = content_type.split(";")

        mime_type = parts[0].strip().casefold()
        charset = None

        for parameter in parts[1:]:
            key, separator, value = parameter.partition("=")

            if separator and key.strip().casefold() == "charset":
                charset = value.strip().strip('"')

        return mime_type, charset
