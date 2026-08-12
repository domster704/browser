from dataclasses import replace
from enum import Enum, auto

from src.domain.entities.html_document import HTMLDocument
from src.domain.html.character_reference import CHARACTER_REFERENCE
from src.domain.html.tokens import (
    BaseToken,
    CharacterToken,
    StartTagToken,
    EndTagToken,
)


class TokenizerState(Enum):
    DATA = auto()
    TAG_OPEN = auto()
    TAG_NAME = auto()
    END_TAG_OPEN = auto()
    CHARACTER_REFERENCE = auto()

    SELF_CLOSING_START_TAG = auto()
    # BOGUS_COMMENT = auto()
    # BEFORE_ATTRIBUTE_NAME = auto()


class HTMLTokenizer:
    """
    Токенизатор HTML-документов - это _state machine, которая разбивает HTML-документ на токены.
    """

    def __init__(self, document: HTMLDocument):
        self._document = document
        self._position = 0
        self._state = TokenizerState.DATA

        self._tokens: list[BaseToken] = []
        self._current_token: BaseToken | None = None
        self._character_reference: str = ""

    def _current_char(self) -> str:
        return self._document.source[self._position]

    def _consume(self) -> None:
        self._position += 1

    def tokenize(self):
        while self._position < len(self._document.source):
            char = self._document.source[self._position]

            match self._state:
                case TokenizerState.DATA:
                    self.__handle_data(char)
                case TokenizerState.TAG_OPEN:
                    self.__handle_tag_open(char)
                case TokenizerState.TAG_NAME:
                    self.__handle_tag_name(char)
                case TokenizerState.END_TAG_OPEN:
                    self.__handle_end_tag_open(char)
                case TokenizerState.CHARACTER_REFERENCE:
                    self.__handle_character_reference(char)
                case TokenizerState.SELF_CLOSING_START_TAG:
                    self.__handle_self_closing_start_tag(char)

        return self._tokens

    def __handle_data(self, char):
        if char == "<":  # <d, <p, <h и т.д.
            self._state = TokenizerState.TAG_OPEN
        elif char == "&":  # &nbsp;, &lt;, &gt;, &amp;
            self._character_reference = ""
            self._state = TokenizerState.CHARACTER_REFERENCE
        else:  # обычный символ
            self._tokens.append(CharacterToken(data=char))

        self._consume()

    def __handle_tag_open(self, char):
        if char == "/":  # </ - начало закрывающего тег
            self._state = TokenizerState.END_TAG_OPEN
            self._consume()
        elif char.isalpha():  # <d, <h, <p и т.д.
            self._current_token = StartTagToken(name="")
            self._state = TokenizerState.TAG_NAME
        elif char == "!":  # <!DOCTYPE, <!--
            raise NotImplementedError("Markup declarations are not supported yet")
        elif char == "?":
            raise NotImplementedError("Bogus comments are not supported yet")
        else:  # 1 < 2, где "<" - это обычный символ текста
            self._tokens.append(CharacterToken(data=char))
            self._state = TokenizerState.DATA

    def __handle_end_tag_open(self, char):
        if char.isalpha():
            self._current_token = EndTagToken(name="")
            self._state = TokenizerState.TAG_NAME
        elif char == ">":
            # missing-end-tag-name parse error
            self._state = TokenizerState.DATA
            self._consume()
        else:
            raise NotImplementedError("Bogus comment _state is not supported yet")

    def __handle_tag_name(self, char):
        if self._current_token is None:
            raise RuntimeError("TAG_NAME _state requires a current token")
        if not isinstance(
            self._current_token,
            (
                StartTagToken,
                EndTagToken,
            ),
        ):
            raise RuntimeError(
                f"TAG_NAME expected StartTagToken or EndTagToken, got {type(self._current_token)}"
            )

        if char == "/":  # self-closing tag
            if not isinstance(self._current_token, StartTagToken):
                raise NotImplementedError(
                    "Self-closing end tags are not supported for non-start tags"
                )
            self._state = TokenizerState.SELF_CLOSING_START_TAG
            self._consume()
            return

        if char == ">":  # окончание тега
            self._tokens.append(self._current_token)
            self._current_token = None
            self._state = TokenizerState.DATA

            self._consume()
            return

        self._current_token = replace(
            self._current_token, name=self._current_token.name + char.casefold()
        )
        self._consume()

    def __handle_character_reference(self, char):
        if char == ";":  # конец сущности
            entity = self._character_reference

            if entity in CHARACTER_REFERENCE:
                data = CHARACTER_REFERENCE[entity]
            else:
                data = f"&{entity};"

            self._tokens.append(CharacterToken(data=data))
            self._character_reference = ""
            self._state = TokenizerState.DATA

            self._consume()
            return

        self._character_reference += char
        self._consume()

    def __handle_self_closing_start_tag(self, char):
        if char != ">":
            raise NotImplementedError("Attributes after '/' are not supported yet")

        self._current_token = replace(self._current_token, self_closing=True)
        self._tokens.append(self._current_token)
        self._current_token = None
        self._state = TokenizerState.DATA

        self._consume()
