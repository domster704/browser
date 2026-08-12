from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import CommentToken


def handle_markup_declaration_open(ctx: TokenizerContext, char: str) -> None:
    source = ctx.document.source
    position = ctx.position

    if source.startswith("--", position):
        ctx.current_token = CommentToken(data="")
        ctx.state = TokenizerState.COMMENT_START
        ctx.position += 2
        return

    if source[position : position + 7].lower() == "doctype":
        ctx.state = TokenizerState.DOCTYPE
        ctx.position += 7
        return

    raise NotImplementedError("Bogus comment and CDATA are not supported yet")
