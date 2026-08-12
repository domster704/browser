from dataclasses import replace

from src.domain.html.tokenizer.characters import SPACE_CHARS
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.handlers.data import emit_and_consume_in_data
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import DOCTYPEToken


def handle_doctype(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume_in(TokenizerState.BEFORE_DOCTYPE_NAME)
        return

    # missing-whitespace-before-doctype-name parse error
    ctx.reconsume_in(TokenizerState.BEFORE_DOCTYPE_NAME)


def handle_before_doctype_name(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume()
        return

    if char == ">":
        ctx.current_token = DOCTYPEToken(
            name=None,
            force_quirks=True,
        )

        emit_and_consume_in_data(ctx)
        return

    ctx.current_token = DOCTYPEToken(name=char.casefold())
    ctx.consume_in(TokenizerState.DOCTYPE_NAME)


def handle_doctype_name(ctx: TokenizerContext, char: str) -> None:
    if not isinstance(ctx.current_token, DOCTYPEToken):
        raise TypeError("DOCTYPE_NAME requires DOCTYPEToken")

    if char in SPACE_CHARS:
        ctx.consume_in(TokenizerState.AFTER_DOCTYPE_NAME)
        return

    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    ctx.current_token = replace(
        ctx.current_token,
        name=(ctx.current_token.name or "") + char.casefold(),
    )

    ctx.consume()


def handle_after_doctype_name(ctx: TokenizerContext, char: str) -> None:
    if char in SPACE_CHARS:
        ctx.consume()
        return

    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    raise NotImplementedError("PUBLIC and SYSTEM doctypes are not supported yet")
