from src.domain.html.document import HTMLDocument
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.dispatcher import STATE_HANDLERS, StateHandler
from src.domain.html.tokenizer.tokens import BaseToken


class HTMLTokenizer:
    def __init__(
        self,
        document: HTMLDocument,
    ):
        self._ctx = TokenizerContext(document=document)

    def tokenize(self) -> list[BaseToken]:
        while not self._ctx.eof:
            handler: StateHandler = STATE_HANDLERS[self._ctx.state]

            handler(self._ctx, self._ctx.current_char)

        return self._ctx.tokens
