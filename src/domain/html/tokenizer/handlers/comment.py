from dataclasses import replace

from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.handlers.data import emit_and_consume_in_data
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import CommentToken


def handle_comment_start(ctx: TokenizerContext, char: str) -> None:
    if char == "-":
        ctx.consume_in(TokenizerState.COMMENT_START_DASH)
        return

    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    ctx.switch_to(TokenizerState.COMMENT)


def handle_comment(ctx: TokenizerContext, char: str) -> None:
    if char == "-":
        ctx.consume_in(TokenizerState.COMMENT_END_DASH)
        return

    _append_comment_data(ctx, char)
    ctx.consume()


def handle_comment_start_dash(ctx: TokenizerContext, char: str) -> None:
    if char == "-":
        ctx.consume_in(TokenizerState.COMMENT_END)
        return

    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    _append_comment_data(ctx, "-")
    ctx.reconsume_in(TokenizerState.COMMENT)


def handle_comment_end_dash(ctx: TokenizerContext, char: str) -> None:
    if char == "-":
        ctx.consume_in(TokenizerState.COMMENT_END)
        return

    _append_comment_data(ctx, "-")
    ctx.reconsume_in(TokenizerState.COMMENT)


def handle_comment_end(ctx: TokenizerContext, char: str) -> None:
    if char == ">":
        emit_and_consume_in_data(ctx)
        return

    if char == "-":
        _append_comment_data(ctx, "-")
        ctx.consume()
        return

    _append_comment_data(ctx, "--")
    ctx.reconsume_in(TokenizerState.COMMENT)


def _append_comment_data(ctx: TokenizerContext, data: str) -> None:
    if not isinstance(ctx.current_token, CommentToken):
        raise TypeError("Comment state requires CommentToken")

    ctx.current_token = replace(
        ctx.current_token,
        data=ctx.current_token.data + data,
    )
