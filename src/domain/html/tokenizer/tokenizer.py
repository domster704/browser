from dataclasses import replace
from enum import Enum, auto

from src.domain.html.document import HTMLDocument
from src.domain.html.tokenizer.character_reference import CHARACTER_REFERENCE
from src.domain.html.tokenizer.tokens import (
    BaseToken,
    CharacterToken,
    StartTagToken,
    EndTagToken,
)

SPACE_CHARS = "\t\n\f "


def _is_ascii_alphabet(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z"


class TokenizerState(Enum):
    DATA = auto()
    TAG_OPEN = auto()
    TAG_NAME = auto()
    END_TAG_OPEN = auto()
    CHARACTER_REFERENCE = auto()

    SELF_CLOSING_START_TAG = auto()
    # BOGUS_COMMENT = auto()

    # ATTRIBUTE START
    BEFORE_ATTRIBUTE_NAME = auto()
    ATTRIBUTE_NAME = auto()
    AFTER_ATTRIBUTE_NAME = auto()
    BEFORE_ATTRIBUTE_VALUE = auto()

    ATTRIBUTE_VALUE_DOUBLE_QUOTED = auto()
    ATTRIBUTE_VALUE_SINGLE_QUOTED = auto()
    ATTRIBUTE_VALUE_UNQUOTED = auto()

    AFTER_ATTRIBUTE_VALUE_QUOTED = auto()
    # ATTRIBUTE END


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

        self._current_attribute_name = ""
        self._current_attribute_value = ""

    def _current_char(self) -> str:
        return self._document.source[self._position]

    def _consume(self) -> None:
        self._position += 1

    def tokenize(self):
        while self._position < len(self._document.source):
            char: str = self._document.source[self._position]

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
                case TokenizerState.BEFORE_ATTRIBUTE_NAME:
                    self.__handle_before_attribute_name(char)
                case TokenizerState.ATTRIBUTE_NAME:
                    self.__handle_attribute_name(char)
                case TokenizerState.AFTER_ATTRIBUTE_NAME:
                    self.__handle_after_attribute_name(char)
                case TokenizerState.BEFORE_ATTRIBUTE_VALUE:
                    self.__handle_before_attribute_value(char)
                case TokenizerState.ATTRIBUTE_VALUE_DOUBLE_QUOTED:
                    self.__handle_attribute_value_double_quoted(char)
                case TokenizerState.ATTRIBUTE_VALUE_SINGLE_QUOTED:
                    self.__handle_attribute_value_single_quoted(char)
                case TokenizerState.ATTRIBUTE_VALUE_UNQUOTED:
                    self.__handle_attribute_value_unquoted(char)
                case TokenizerState.AFTER_ATTRIBUTE_VALUE_QUOTED:
                    self.__handle_after_attribute_value_quoted(char)

        return self._tokens

    def __handle_data(self, char: str):
        if char == "<":  # <d, <p, <h и т.д.
            self._state = TokenizerState.TAG_OPEN
        elif char == "&":  # &nbsp;, &lt;, &gt;, &amp;
            self._character_reference = ""
            self._state = TokenizerState.CHARACTER_REFERENCE
        else:  # обычный символ
            self._tokens.append(CharacterToken(data=char))

        self._consume()

    def __handle_tag_open(self, char: str):
        if char == "/":  # </ - начало закрывающего тег
            self._state = TokenizerState.END_TAG_OPEN
            self._consume()
        elif _is_ascii_alphabet(char):  # <d, <h, <p и т.д.
            self._current_token = StartTagToken(name="")
            self._state = TokenizerState.TAG_NAME
        elif char == "!":  # <!DOCTYPE, <!--
            raise NotImplementedError("Markup declarations are not supported yet")
        elif char == "?":
            raise NotImplementedError("Bogus comments are not supported yet")
        else:  # 1 < 2, где "<" - это обычный символ текста
            self._tokens.append(CharacterToken(data=char))
            self._state = TokenizerState.DATA

    def __handle_end_tag_open(self, char: str):
        if _is_ascii_alphabet(char):
            self._current_token = EndTagToken(name="")
            self._state = TokenizerState.TAG_NAME
        elif char == ">":
            # missing-end-tag-name parse error
            self._state = TokenizerState.DATA
            self._consume()
        else:
            raise NotImplementedError("Bogus comment _state is not supported yet")

    def __handle_tag_name(self, char: str):
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
        # Проверка на наличие пробельных символов в имени тега => на атрибуты
        if char in SPACE_CHARS:
            self._state = TokenizerState.BEFORE_ATTRIBUTE_NAME
            self._consume()
            return

        if char == "/":  # self-closing tag
            if not isinstance(self._current_token, StartTagToken):
                raise NotImplementedError(
                    "Self-closing end tags are not supported for non-start tags"
                )
            self.__enter_self_closing_start_tag()
            return

        if char == ">":  # окончание тега
            self.__emit_current_tag()
            return

        self._current_token = replace(
            self._current_token, name=self._current_token.name + char.casefold()
        )
        self._consume()

    def __handle_character_reference(self, char: str):
        # TODO: переделать для случая <a title="Tom &amp; Jerry">
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

    def __handle_self_closing_start_tag(self, char: str):
        if char != ">":
            raise NotImplementedError("Attributes after '/' are not supported yet")

        self._current_token = replace(self._current_token, self_closing=True)
        self._tokens.append(self._current_token)
        self._current_token = None
        self._state = TokenizerState.DATA

        self._consume()

    def __handle_before_attribute_name(self, char: str) -> None:
        if char in SPACE_CHARS:
            self._consume()
            return

        if char == "/":
            self.__enter_self_closing_start_tag()
            return
        if char == ">":
            self.__emit_current_tag()
            return

        self.__start_attribute()

    def __handle_attribute_name(self, char: str) -> None:
        if char in SPACE_CHARS:
            self._state = TokenizerState.AFTER_ATTRIBUTE_NAME
            self._consume()
            return
        if char == "=":
            self._state = TokenizerState.BEFORE_ATTRIBUTE_VALUE
            self._consume()
            return
        if char == "/":
            self.__commit_attribute()
            self.__enter_self_closing_start_tag()
            return
        if char == ">":
            self.__commit_attribute()
            self.__emit_current_tag()
            return

        self._current_attribute_name += char.lower()
        self._consume()

    def __handle_after_attribute_name(self, char: str) -> None:
        if char in SPACE_CHARS:
            self._consume()
            return
        if char == "=":
            self._state = TokenizerState.BEFORE_ATTRIBUTE_VALUE
            self._consume()
            return
        if char == "/":
            self.__commit_attribute()
            self.__enter_self_closing_start_tag()
            return
        if char == ">":
            self.__commit_attribute()
            self.__emit_current_tag()
            return

        self.__commit_attribute()
        self.__start_attribute()

    def __handle_before_attribute_value(self, char: str) -> None:
        if char in SPACE_CHARS:
            self._consume()
            return
        if char == '"':
            self._state = TokenizerState.ATTRIBUTE_VALUE_DOUBLE_QUOTED
            self._consume()
            return
        if char == "'":
            self._state = TokenizerState.ATTRIBUTE_VALUE_SINGLE_QUOTED
            self._consume()
            return
        if char == ">":
            self.__commit_attribute()
            self.__emit_current_tag()
            return
        self._state = TokenizerState.ATTRIBUTE_VALUE_UNQUOTED

    def __handle_attribute_value_double_quoted(self, char: str) -> None:
        self.__handle_attribute_value_quoted(char=char, quote='"')

    def __handle_attribute_value_single_quoted(self, char: str) -> None:
        self.__handle_attribute_value_quoted(char=char, quote="'")

    def __handle_attribute_value_quoted(self, char: str, quote: str) -> None:
        if char == quote:
            self.__commit_attribute()
            self._state = TokenizerState.AFTER_ATTRIBUTE_VALUE_QUOTED
            self._consume()
            return

        self._current_attribute_value += char
        self._consume()

    def __handle_attribute_value_unquoted(self, char: str) -> None:
        if char in SPACE_CHARS:
            self.__commit_attribute()
            self._state = TokenizerState.BEFORE_ATTRIBUTE_NAME
            self._consume()
            return
        if char == ">":
            self.__commit_attribute()
            self.__emit_current_tag()
            return

        self._current_attribute_value += char
        self._consume()

    def __handle_after_attribute_value_quoted(self, char: str) -> None:
        if char in SPACE_CHARS:
            self._state = TokenizerState.BEFORE_ATTRIBUTE_NAME
            self._consume()
            return
        if char == "/":
            self.__enter_self_closing_start_tag()
            return
        if char == ">":
            self.__emit_current_tag()
            return

        self._state = TokenizerState.BEFORE_ATTRIBUTE_NAME

    def __commit_attribute(self):
        if not isinstance(self._current_token, StartTagToken):
            raise RuntimeError("Attribute can only be committed to StartTagToken")

        if not self._current_attribute_name:
            return

        attributes = dict(self._current_token.attributes)
        if self._current_attribute_name not in attributes:
            attributes[self._current_attribute_name] = self._current_attribute_value

        self._current_token = replace(self._current_token, attributes=attributes)

        self._current_attribute_name = ""
        self._current_attribute_value = ""

    def __emit_current_tag(self) -> None:
        if self._current_token is None:
            raise RuntimeError("No current tag token")

        self._tokens.append(self._current_token)
        self._current_token = None
        self._state = TokenizerState.DATA
        self._consume()

    def __enter_self_closing_start_tag(self) -> None:
        self._state = TokenizerState.SELF_CLOSING_START_TAG
        self._consume()

    def __start_attribute(self) -> None:
        self._current_attribute_name = ""
        self._current_attribute_value = ""
        self._state = TokenizerState.ATTRIBUTE_NAME
