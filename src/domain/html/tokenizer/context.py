from dataclasses import dataclass, field

from src.domain.html.document import HTMLDocument
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import BaseToken


@dataclass
class TokenizerContext:
    document: HTMLDocument

    position: int = 0
    state: TokenizerState = TokenizerState.DATA

    tokens: list[BaseToken] = field(default_factory=list)

    current_token: BaseToken | None = None

    character_reference: str = ""

    current_attribute_name: str = ""
    current_attribute_value: str = ""

    @property
    def current_char(self) -> str:
        return self.document.source[self.position]

    @property
    def eof(self) -> bool:
        return self.position >= len(self.document.source)

    def consume(self) -> None:
        self.position += 1

    def consume_in(self, state: TokenizerState) -> None:
        self.state = state
        self.consume()

    def reconsume_in(self, state: TokenizerState) -> None:
        self.switch_to(state)

    def switch_to(self, state: TokenizerState) -> None:
        self.state = state

    def emit(self, token: BaseToken) -> None:
        self.tokens.append(token)

    def emit_current_token(self) -> None:
        if self.current_token is None:
            raise RuntimeError("No current token")

        self.emit(self.current_token)
        self.current_token = None
