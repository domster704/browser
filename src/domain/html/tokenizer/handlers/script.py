from src.domain.html.tokenizer.characters import SPACE_CHARS
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import CharacterToken, EndTagToken


def handel_script_data(ctx: TokenizerContext, char: str):
    if char == "<":
        if _try_consume_script_end_tag(ctx):
            return

        ctx.emit(CharacterToken(data="<"))
        ctx.consume()
        return

    ctx.emit(CharacterToken(data=char))
    ctx.consume()


def _try_consume_script_end_tag(ctx: TokenizerContext) -> bool:
    source = ctx.document.source
    position = ctx.position

    end_script_tag = "</script"

    if source[position : position + len(end_script_tag)].casefold() != end_script_tag:
        return False

    position += len(end_script_tag)
    if position >= len(source):
        return False

    char = source[position]
    if char not in SPACE_CHARS and char != ">":
        return False

    while position < len(source) and source[position] in SPACE_CHARS:
        position += 1

    if position >= len(source):
        return False
    if source[position] != ">":
        return False

    ctx.emit(EndTagToken(name="script"))
    ctx.position = position + 1
    ctx.switch_to(TokenizerState.DATA)

    return True
