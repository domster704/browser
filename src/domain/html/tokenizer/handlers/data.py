from src.domain.html.tokenizer.characters import CHARACTER_REFERENCE
from src.domain.html.tokenizer.context import TokenizerContext
from src.domain.html.tokenizer.state import TokenizerState
from src.domain.html.tokenizer.tokens import CharacterToken


def handle_data(ctx: TokenizerContext, char: str):
    if char == "<":  # <d, <p, <h и т.д.
        ctx.switch_to(TokenizerState.TAG_OPEN)
    elif char == "&":  # &nbsp;, &lt;, &gt;, &amp;
        ctx.character_reference = ""
        ctx.switch_to(TokenizerState.CHARACTER_REFERENCE)
    else:  # обычный символ
        ctx.emit(CharacterToken(data=char))

    ctx.consume()


def handle_character_reference(ctx: TokenizerContext, char: str):
    # TODO: переделать для случая <a title="Tom &amp; Jerry">
    if char == ";":  # конец сущности
        entity = ctx.character_reference

        if entity in CHARACTER_REFERENCE:
            data = CHARACTER_REFERENCE[entity]
        else:
            data = f"&{entity};"

        ctx.emit(CharacterToken(data=data))
        ctx.character_reference = ""
        ctx.consume_in(TokenizerState.DATA)
        return

    ctx.character_reference += char
    ctx.consume()


def emit_and_consume_in_data(ctx: TokenizerContext):
    ctx.emit_current_token()
    ctx.consume_in(TokenizerState.DATA)
