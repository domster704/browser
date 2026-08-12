from dataclasses import replace

from src.domain.html.tokenizer.characters import SPACE_CHARS
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.handlers.data import emit_and_consume_in_data
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import StartTagToken


def handle_before_attribute_name(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume()
        return

    if char == "/":
        ctx.consume_in(TokenizerState.SELF_CLOSING_START_TAG)
        return
    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    _start_attribute(ctx)


def handle_attribute_name(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.switch_to(TokenizerState.AFTER_ATTRIBUTE_NAME)
        ctx.consume()
        return
    if char == "=":
        ctx.switch_to(TokenizerState.BEFORE_ATTRIBUTE_VALUE)
        ctx.consume()
        return
    if char == "/":
        _commit_attribute(ctx)
        ctx.consume_in(TokenizerState.SELF_CLOSING_START_TAG)
        return
    if char == ">":
        _commit_attribute(ctx)
        emit_and_consume_in_data(ctx)
        return

    ctx.current_attribute_name += char.lower()
    ctx.consume()


def handle_after_attribute_name(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume()
        return
    if char == "=":
        ctx.consume_in(TokenizerState.BEFORE_ATTRIBUTE_VALUE)
        return
    if char == "/":
        _commit_attribute(ctx)
        ctx.consume_in(TokenizerState.SELF_CLOSING_START_TAG)
        return
    if char == ">":
        _commit_attribute(ctx)
        emit_and_consume_in_data(ctx)
        return

    _commit_attribute(ctx)
    _start_attribute(ctx)


def handle_before_attribute_value(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume()
        return
    if char == '"':
        ctx.consume_in(TokenizerState.ATTRIBUTE_VALUE_DOUBLE_QUOTED)
        return
    if char == "'":
        ctx.consume_in(TokenizerState.ATTRIBUTE_VALUE_SINGLE_QUOTED)
        return
    if char == ">":
        _commit_attribute(ctx)
        emit_and_consume_in_data(ctx)
        return

    ctx.reconsume_in(TokenizerState.ATTRIBUTE_VALUE_UNQUOTED)


def handle_attribute_value_double_quoted(ctx: TokenizerContext, char: str) -> None:
    _handle_attribute_value_quoted(ctx, char=char, quote='"')


def handle_attribute_value_single_quoted(ctx: TokenizerContext, char: str) -> None:
    _handle_attribute_value_quoted(ctx, char=char, quote="'")


def _handle_attribute_value_quoted(
    ctx: TokenizerContext, char: str, quote: str
) -> None:
    if char == quote:
        _commit_attribute(ctx)
        ctx.consume_in(TokenizerState.AFTER_ATTRIBUTE_VALUE_QUOTED)
        return

    ctx.current_attribute_value += char
    ctx.consume()


def handle_attribute_value_unquoted(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        _commit_attribute(ctx)
        ctx.consume_in(TokenizerState.BEFORE_ATTRIBUTE_NAME)
        return
    if char == ">":
        _commit_attribute(ctx)

        emit_and_consume_in_data(ctx)
        return

    ctx.current_attribute_value += char
    ctx.consume()


def handle_after_attribute_value_quoted(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume_in(TokenizerState.BEFORE_ATTRIBUTE_NAME)
        return
    if char == "/":
        ctx.consume_in(TokenizerState.SELF_CLOSING_START_TAG)
        return
    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    ctx.reconsume_in(TokenizerState.BEFORE_ATTRIBUTE_NAME)


def _commit_attribute(ctx: TokenizerContext):
    if not isinstance(ctx.current_token, StartTagToken):
        raise TypeError("Attribute can only be committed to StartTagToken")

    if not ctx.current_attribute_name:
        return

    attributes = dict(ctx.current_token.attributes)
    if ctx.current_attribute_name not in attributes:
        attributes[ctx.current_attribute_name] = ctx.current_attribute_value

    ctx.current_token = replace(
        ctx.current_token,
        attributes=attributes,
    )

    ctx.current_attribute_name = ""
    ctx.current_attribute_value = ""


def _start_attribute(ctx: TokenizerContext) -> None:
    ctx.current_attribute_name = ""
    ctx.current_attribute_value = ""
    ctx.reconsume_in(TokenizerState.ATTRIBUTE_NAME)
