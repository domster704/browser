from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Resource:
    body: bytes
    mime_type: str | None = None
    charset: str | None = None

    def decode(self) -> str:
        return self.body.decode(self.charset or "utf-8")
