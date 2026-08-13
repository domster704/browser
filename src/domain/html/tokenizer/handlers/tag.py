from dataclasses import replace

from src.domain.html.tokenizer.characters import SPACE_CHARS, _is_ascii_alphabet
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.handlers.data import emit_and_consume_in_data
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import CharacterToken, EndTagToken, StartTagToken


def handle_tag_open(ctx: TokenizerContext, char: str):
    if char == "/":  # </ - начало закрывающего тег
        ctx.consume_in(TokenizerState.END_TAG_OPEN)
    elif _is_ascii_alphabet(char):  # <d, <h, <p и т.д.
        ctx.current_token = StartTagToken(name="")
        ctx.switch_to(TokenizerState.TAG_NAME)
    elif char == "!":  # <!DOCTYPE, <!--
        ctx.consume_in(TokenizerState.MARKUP_DECLARATION_OPEN)
    elif char == "?":
        raise NotImplementedError("Bogus comments are not supported yet")
    else:  # 1 < 2, где "<" - это обычный символ текста
        ctx.emit(CharacterToken(data=char))
        ctx.switch_to(TokenizerState.DATA)


def handle_end_tag_open(ctx: TokenizerContext, char: str):
    if _is_ascii_alphabet(char):
        ctx.current_token = EndTagToken(name="")
        ctx.switch_to(TokenizerState.TAG_NAME)
    elif char == ">":
        # missing-end-tag-name parse error
        ctx.consume_in(TokenizerState.DATA)
    else:
        raise NotImplementedError("Bogus comment _state is not supported yet")


def handle_tag_name(ctx: TokenizerContext, char: str):
    if ctx.current_token is None:
        raise RuntimeError("TAG_NAME _state requires a current token")
    if not isinstance(
        ctx.current_token,
        (StartTagToken, EndTagToken),
    ):
        raise TypeError(
            f"TAG_NAME expected StartTagToken or EndTagToken, got {type(ctx.current_token)}"
        )
    # Проверка на наличие пробельных символов в имени тега => на атрибуты
    if char in SPACE_CHARS:
        ctx.consume_in(TokenizerState.BEFORE_ATTRIBUTE_NAME)
        return

    if char == "/":  # self-closing tag
        if not isinstance(ctx.current_token, StartTagToken):
            raise NotImplementedError(
                "Self-closing end tags are not supported for non-start tags"
            )
        ctx.consume_in(TokenizerState.SELF_CLOSING_START_TAG)
        return

    if char == ">":  # окончание тега
        emit_and_consume_in_data(ctx)
        return

    ctx.current_token = replace(
        ctx.current_token,
        name=ctx.current_token.name + char.casefold(),
    )
    ctx.consume()


def handle_self_closing_start_tag(ctx: TokenizerContext, char: str):
    if char != ">":
        raise NotImplementedError("Attributes after '/' are not supported yet")

    if not isinstance(ctx.current_token, StartTagToken):
        raise TypeError("Expected StartTagToken")

    ctx.current_token = replace(
        ctx.current_token,
        self_closing=True,
    )
    emit_and_consume_in_data(ctx)
