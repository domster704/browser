from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class BaseToken:
    pass


@dataclass(frozen=True, slots=True)
class StartTagToken(BaseToken):
    name: str
    attributes: dict[str, str] = field(default_factory=dict)
    self_closing: bool = False


@dataclass(frozen=True, slots=True)
class EndTagToken(BaseToken):
    name: str


@dataclass(frozen=True, slots=True)
class CharacterToken(BaseToken):
    data: str


@dataclass(frozen=True, slots=True)
class CommentToken(BaseToken):
    data: str


@dataclass(frozen=True, slots=True)
class DOCTYPEToken(BaseToken):
    name: str | None
    public_identifier: str | None = None
    system_identifier: str | None = None
    force_quirks: bool = False


@dataclass(frozen=True, slots=True)
class EOFToken(BaseToken):
    pass
