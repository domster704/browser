from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import SplitResult, urlsplit


@dataclass(frozen=True, slots=True)
class URI:
    scheme: str
    host: str | None
    port: int | None
    path: str
    query: str | None = None
    fragment: str | None = None

    @classmethod
    def parse(cls, raw: str) -> URI:
        result: SplitResult = urlsplit(raw)
        if not result.scheme:
            raise ValueError("URI must contain scheme")

        path = result.path or "/"

        return cls(
            scheme=result.scheme.casefold(),
            host=result.hostname,
            port=result.port,
            path=path,
            query=result.query or None,
            fragment=result.fragment or None,
        )
