from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Resource:
    body: bytes
    mime_type: str | None = None
    charset: str | None = None
